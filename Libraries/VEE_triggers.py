"""
"""

from utils.threads import VDOM_thread

import VEE_core


APP_ID = application.id


class EngineTimeTrigger(VDOM_thread):
    '''
    '''
    DEFAULT_TIMEOUT = 5.0

    def __init__(self):
        VDOM_thread.__init__(self)

    def work(self):
        '''
        '''
        try:
            #debug("------------>>>> Trying to start engine: ")
            application.set_app_id(APP_ID)
            self.save_thread()

            return VEE_core.engine.process_queue() or self.DEFAULT_TIMEOUT
            
        except Exception as ex:
            VEE_core.engine.engine_logger.exception('')
#           from vdom_trace import Trace
#           VEE_core.engine.log("@@@@@@@@@Error while vscript execution." )
#           VEE_core.engine.log( Trace.exception_trace() )

            # try:
            #   VEE_core.engine.info( str( e ) )
            # except: pass
            # #debug("------------>>>> Exception: %s"%e)
            try:
                return self.DEFAULT_TIMEOUT

            except Exception as ex:
                self.stop()


    def save_thread(self):
        '''
        '''
        try:
            import VEE_core as c
            c.engine_thread = self
        except:
            pass


class CompilerTimeTrigger(VDOM_thread):
    '''
    '''
    DEFAULT_TIMEOUT = 5.0

    def __init__(self):
        VDOM_thread.__init__(self)

    def work(self):
        '''
        '''
        try:
            #debug("------------>>>> Trying to start engine: ")
            application.set_app_id(APP_ID)
            self.save_thread()

            return VEE_core.engine.do_compile() or self.DEFAULT_TIMEOUT
            
        except Exception as ex:
            VEE_core.engine.engine_logger.exception('')
            # from vdom_trace import Debug
            # VEE_core.engine.error_log()
            # VEE_core.engine.info( Debug.exception_trace_s() )

            # try:
            #   VEE_core.engine.info( str( e ) )
            # except: pass
            # #debug("------------>>>> Exception: %s"%e)
            try:
                return self.DEFAULT_TIMEOUT

            except Exception as ex:
                self.stop()


    def save_thread(self):
        '''
        '''
        try:
            import VEE_core as c
            c.compiler_thread = self
        except:
            pass