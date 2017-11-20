from collections import deque
from VEE_events import VEE_StopEngineEvent, VEE_TimerEvent, \
                       VEE_StartEngineEvent, VEE_BaseAbstractEvent
from VEE_timer import VEE_timer
from VEE_logs import EngineMessage
from VEE_utils import encodeUTF8
from datetime import datetime
import Queue
import logging
from prosuite_logging import DequeMemoryHandler, app_logger as root_logger


MAX_LOG_LEN = 200

disable = getattr(application, 'ENV_DISABLE_VSCRIPT', False)

workflow_queue  = Queue.Queue()
compiler_queue  = Queue.Queue()
queue_thread = None
compiler_thread = None

class VdomEventEngine:
    def __init__( self ):
        self.listeners          = {}
        self.timers             = {}
        self.setup_logging()
        self.engine_start()

    def setup_logging(self):
        '''
        '''
        memory_hdlr = DequeMemoryHandler(capacity=MAX_LOG_LEN)
        self.logs = memory_hdlr

        self.engine_logger = root_logger.getChild('Engine')
        self.engine_logger.addHandler(memory_hdlr)
        self.engine_logger.setLevel(logging.DEBUG)
        self.engine_logger.info('Engine logger initialized!')

        self.plugin_logger = root_logger.getChild('Plugin')
        self.plugin_logger.addHandler(memory_hdlr)
        self.plugin_logger.setLevel(logging.DEBUG)
        self.plugin_logger.info('Plugin logger initialized!')

    def engine_start( self ):
        if disable:
            return

        from VEE_time_trigger import engineTimeTrigger
        from VEE_compiler_trigger import compilerTimeTrigger
        self.put_event( VEE_StartEngineEvent() )

        self.engine_logger.info("Starting engine thread...")
        engineTimeTrigger().start()

        self.engine_logger.info("Starting compiler thread...")
        compilerTimeTrigger().start()

        self.engine_logger.info(  u"Engine started." )


    def engine_stop( self ):
        self.engine_logger.info(  u"Engine stopped." )
        if queue_thread:
            queue_thread.stop()
        if compiler_thread:
            compiler_thread.stop()
        self.clear_all()


    def load_listeners( self ):
        from class_macro import register_all_event_macro
        register_all_event_macro()


    def put_event( self, event ):
        # enqueue application events only if there are listeners for them
        if isinstance(event, VEE_BaseAbstractEvent) and \
            (event.__class__, hash(event)) not in self.listeners:
            return
        workflow_queue.put( event )


    def process_queue( self ):
        event = None
        try:
            event = workflow_queue.get( True, 5 )
        except Queue.Empty:
            self.check_timers()
            return 2.0

        if isinstance( event, VEE_TimerEvent ):
            self.engine_logger.info(  u"Recieved event of class '{timeClass}' with name '{timerName}'".format(
                        timeClass = event.__class__.__name__[ 4: ],
                        timerName = event.timer.timer.name.split( ":", 1 )[ 1 ] ) )

        else:
            self.info( ( u"Recieved event of class '{className}' ({cls}:{hash})".format(
                       className = event.__class__.__name__[ 4: ],
                       cls = event.__class__.__name__,
                       hash = hash( event ) ) ) )
            self.engine_logger.info( ( u"Recieved event of class '{className}'".format(
                        className = event.__class__.__name__[ 4: ]  ) ) )


            if isinstance( event, VEE_StopEngineEvent ):
                self.engine_stop()
                return

            elif isinstance( event, VEE_StartEngineEvent ):
                self.load_listeners()
                return

        key = ( event.__class__, hash( event ) )
        if key in self.listeners:
            dispatchers = self.listeners[ key ]
            self.engine_logger.info(  u"Event '{className}' has {dispatchersCount} dispatchers".format(
                        className = event.__class__.__name__[4:],
                        dispatchersCount = len( dispatchers ) ) )

            for dispatcher in dispatchers.itervalues():
                dispatcher( event )

        else:
            self.engine_logger.info(  u"No dispatcher for given event '{className}'".format(
                        className = event.__class__.__name__[4:] ) )

        #check for webdav activity
#        try:
#            from webdav_server.vdom_dav_provider import get_properties
#            if (datetime.now() - get_properties.last_access()).total_seconds()<30:
#                return 10.0
#        except Exception as e:
#            return 1.0

        return 0.25

    def get_dispatcher_by_event( self, event ):
        key = ( event.__class__, hash( event ) )
        if key in self.listeners:
            return self.listeners[ key ].values()[ 0 ]

        return None

    def do_compile(self):
        task = None
        try:
            task = compiler_queue.get( True, 5 )
        except Queue.Empty:
            return

        macro, event_class, key, dispatcher =  task
        self.engine_logger.debug("%s[%s] - start compiling", macro.name, macro.guid)
        ret = dispatcher.compile()
        if ret == COMPILATION_SUCCESS:
            self.compile_done(macro, event_class, key, dispatcher)
            self.engine_logger.debug("%s[%s] - compiling done", macro.name, macro.guid)
#             self.engine_logger.info("Compiling done" )
        else:
            self.engine_logger.debug("%s[%s] - compiling failing", macro.name, macro.guid)
#             self.engine_logger.info("Compiling failed" )
        #cache, code = compile( source , environment = env )

    def compile_done(self, macro, event_class, key, dispatcher):
        macro.bytecode = (dispatcher.cache, dispatcher.debuginfo)
        macro.save_after_compile()
        self.register_dispatcher(event_class, key, dispatcher)

    def compile_and_register(self, macro, event_class, key):
        try:
            dispatcher = VEE_vmacro_dispatcher(macro)
            if macro.bytecode:
                self.engine_logger.debug("%s[%s] - bytecode exists", macro.name, macro.guid)
                self.register_dispatcher(event_class, key, dispatcher)
                return COMPILATION_SUCCESS

            self.engine_logger.debug("%s[%s] - put macro in compile queue", macro.name, macro.guid)
            compiler_queue.put((macro, event_class, key, dispatcher))

        except Exception as e:
            self.engine_logger.exception("@@@@@@@@@Error while vscript compilation." )


    def register_dispatcher( self, event_class, event_key, dispatcher ):
        key = ( event_class, event_key )
        disp_hash = hash( dispatcher.guid )
        self.info(  u"Register dispatcher '{dispatcherName}' for event '{eventName}' ({cls}:{hash})".format(
                       dispatcherName = dispatcher.name,
                       eventName = event_class.__name__[ 4: ],
                       cls = event_class.__name__,
                       hash = event_key ) )

        self.engine_logger.info(  u"Register dispatcher '{dispatcherName}' for event '{eventName}'".format(
                        dispatcherName = dispatcher.name,
                        eventName = event_class.__name__[ 4: ] ) )


        if key not in self.listeners:
            self.listeners[ key ] = {}

        self.listeners[ key ][ disp_hash ] = dispatcher


    def unregister_dispatcher( self, event_class, event_key, disp_guid ):
        key = ( event_class, event_key )
        if key in self.listeners:
            dispatchers = self.listeners[ key ]
            disp_hash = hash( disp_guid )

            if disp_hash in dispatchers:
                dispatcher = dispatchers[ disp_hash  ]
                del dispatchers[ disp_hash ]

                self.engine_logger.info(  u"Unregister dispatcher '{dispatcherName}' for event '{eventName}'".format(
                                dispatcherName = dispatcher.name,
                                eventName = event_class.__name__[ 4: ] ) )


            if len( dispatchers ) == 0:
                del self.listeners[ key ]


    def clear_all(self):
        self.clear_log()
        self.listeners = {}
        self.timers = {}
        try:
            while True:
                workflow_queue.get_nowait()
        except Queue.Empty:
            pass


    def add_timer( self, name, delay, hash_value ):
        """Add timer with defined name and delay"""
        if name not in self.timers:
            self.timers[ name ] = VEE_timer( name, delay, hash_value )


    def update_timer( self, name, delay, hash_value ):
        """Replace timer with defined name and delay"""
        self.timers[name] = VEE_timer( name, delay, hash_value )


    def delete_timer( self, name ):
        """Removing timer. If there is no with such name - no exception rising"""
        try:
            del self.timers[ name ]
        except Exception:
            pass


    def activate_timer( self, name, state ):
        """Timer change state to active. If there is no with such name - exception raised"""
        try:
            self.timers[ name ].active = state
        except Exception:
            raise Exception( "No timer with such name" )


    def check_timers(self):
        for timer_name in self.timers:
            if self.timers[ timer_name ].check():
                self.put_event( VEE_TimerEvent( self.timers[ timer_name ] ) )


    def get_timer_by_name( self, name ):
        return self.timers.get( name, None )


engine = VdomEventEngine()
from VEE_vmacro_dispatcher import VEE_vmacro_dispatcher,  COMPILATION_SUCCESS
