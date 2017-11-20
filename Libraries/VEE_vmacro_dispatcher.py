#23.01.2013
#clean library

#from VEE_logs import PluginMessage, PluginMessageError
from VEE_tools import 	compile, execute, PythonCompilationError, VScriptComlipationError,\
						PythonExecutionError, VScriptExecutionError, StopExecutionError

from VEE_events import VEE_TimerEvent
from VEE_sqlite3 import v_DatabaseManager
from VEE_resources import v_ResManager, v_TempResManager

from functools import partial
import VEE_std_lib, VEE_proadmin, VEE_system, VEE_urllib, VEE_server
#import promail_wrappers

import VEE_appinmail


vscript_wrappers_name="wrappers"

EXECUTION_FAILED = 1
COMPILATION_FAILED = 2
EXECUTION_SUCCESS = 3
COMPILATION_SUCCESS = 4


STD_ENV_DICT = 	VEE_std_lib.environment + VEE_proadmin.environment \
				+ VEE_system.environment + VEE_urllib.environment + VEE_server.environment \
				+ VEE_appinmail.environment

APP_ENV_DICT = 	tuple()

WHOLE_ENV_DICT = (
					(	"v_wholeconnection"				, vscript_wrappers_name ),
					(	"v_wholeapplication"			, vscript_wrappers_name ),
					(	"v_wholeerror"					, vscript_wrappers_name ),
					(	"v_wholeconnectionerror"		, vscript_wrappers_name ),
					(	"v_wholenoconnectionerror"		, vscript_wrappers_name ),
					(	"v_wholeremotecallerror"		, vscript_wrappers_name ),
					(	"v_wholeincorrectresponse"		, vscript_wrappers_name ),
					(	"v_wholenoapierror"				, vscript_wrappers_name ),
					(	"v_wholenoapplication"			, vscript_wrappers_name ),
				)



class VEE_vmacro_dispatcher:

	def __init__( self, macros ):
		self.code 		= macros.code
		self.name 		= macros.name
		self.lib_code   = self.insert_libraries(macros)
		self.namespace 	= macros.plugin_guid
		self.guid		= macros.guid
		self.debug 		= True
		if isinstance(macros.bytecode, tuple):
			self.cache, self.debuginfo = macros.bytecode
		else:
			self.cache = macros.bytecode
			self.debuginfo = []
		self.logger     = engine.plugin_logger.getChild(macros.get_plugin().name).getChild(self.name)


	def __hash__( self ):
		return hash( self.guid )


	def __str__( self ):
		return u"{0}:{1}".format( self.namespace, self.name ).encode( "utf8" )


	def __repr__( self ):
		return u"{0}:{1}".format( self.namespace, self.name ).encode( "utf8" )


	def __call__( self, event = None, env_mask = 0b1011, custom_env = None, safe = True ):
		return self.__execute_script( self.environment(event, env_mask, custom_env), safe )

	def environment(self, event = None, env_mask = 0b1011, custom_env = None):
#		env_mask values:
#			0b0001 		- WHOLE_ENV
#			0b0010 		- STD_ENV + APP_ENV
#			0b0011		- STD_ENV + WHOLE_ENV + APP_ENV
#			0b0100		- CUSTOM_ENV
#			0b0111		- CUSTOM_ENV + STD_ENV + WHOLE_ENV + APP_ENV
#			0b1000		- !!!only for EVENT MACROS - initialize v_event variable

		env = []

		if env_mask & 0b0001:
			env += WHOLE_ENV_DICT

		if env_mask & 0b0010:

			v_plugin = VEE_std_lib.v_plugin( self.namespace )
			v_macros = VEE_std_lib.v_macros( self.guid, self.name )

			env += 	STD_ENV_DICT + (
							(	"v_dbdictionary"  			, VEE_std_lib.v_dbdictionary( self.namespace ) 					),
							(	"v_logger"					, partial( VEE_system.v_system.log, disp = self )				),
							(	"v_log"						, partial( VEE_system.v_system.log, disp = self )				), #need to delete
							( 	"v_clearlog"				, partial( VEE_system.v_system.v_clearlog, disp = self )		),
							(	"v_activatetimer"			, partial( VEE_std_lib.v_engine.v_activatetimer, disp = self ) 	),
							(	"v_deactivatetimer"			, partial( VEE_std_lib.v_engine.v_deactivatetimer, disp = self )),
							( 	"v_gettimer"				, partial( VEE_std_lib.v_engine.v_gettimer, disp = self ) 		),
							( 	"v_database"				, v_DatabaseManager( self.namespace ) 							),
							(	"v_resources"				, v_ResManager( self.namespace ) 								),
							(	"v_tempresources"			, v_TempResManager( self.namespace ) 							),
							( 	"v_customevent"				, VEE_std_lib.v_customevent 									),
							(	"v_raiseevent"				, partial( VEE_std_lib.v_raiseevent, disp = self ) 				),
							(	"v_plugin"					, v_plugin														),
							( 	"v_macros"					, v_macros														),
						) + APP_ENV_DICT

			VEE_system.v_system.debug 			= partial( VEE_system.v_system.debug, disp = self )


		if env_mask & 0b0100:
			env += custom_env if custom_env else []
		else:
			env +=(#Empty wrappers to register names in namespace
			( "v_page_status", None),
			( "v_currentpage", None),
			( "v_xml_dialog", None),
			( "v_xmldialog", None),
			( "v_sessiondictionary", None),
			( "v_showgrowl", None),
			( "v_response", None),
										)

		# add EAC
#		env += ( ( "v_eac", promail_wrappers.v_EAC), )

		# add ProMail
#		if not filter(lambda x: x[0] == 'v_promail', env):
#			env += ( ( "v_promail", promail_wrappers.MacroParameters({})), )

		if env_mask & 0b1000:
			env += ( ( "v_timerevent", event.timer ) \
							if isinstance( event, VEE_TimerEvent ) else \
					 ( "v_event", VEE_std_lib.v_event( event ) ), )
		return dict( env )



	def insert_libraries(self, macros):
		self.libraries, line, libs = [], 1, u""

		for lib in macros.libraries():
			next_line = line + lib.code.count("\n") + 1
			self.libraries.append( ( lib.name, (line, next_line - 1)))
			line = next_line
			libs += lib.code + u"\n"

		return libs


	def parse_error(self, error, title):
		try:
			error_line = int(error.line)
		except Exception as ex:
			self.error('Parse error line \"{}\": {}'.format(error.line, ex))
			error_line = 0
		lib_name = ""

		if self.libraries:
			max_line = 0
			for lib in self.libraries:
				max_line = max_line if max_line >= lib[1][1] else lib[1][1]
				if lib[1][0] <= error_line <= lib[1][1]:
					lib_name = lib[0]
					error_line = error_line - lib[1][0] + 1
					break

			if not lib_name:
				error_line = error_line - max_line

		if lib_name: lib_name = u"Library '{0}', ".format(lib_name)

		self.error( u"{title} ({lib}Line {line}): {msg}".format(
							title = title,
							lib = lib_name,
							line = error_line,
							msg  = error.message ) )


	def compile( self):

		env = self.environment()
		try:
			self.info( u"VScript Compiler Start" )
			self.cache, self.debuginfo = compile( self.lib_code + self.code , environment = env )
			self.lib_code = None
			self.info( u"VScript Compiler Finish" )
			return COMPILATION_SUCCESS

		except VScriptComlipationError as error:
			self.parse_error(error, "VScript Compilation Error")
			return COMPILATION_FAILED

		except PythonCompilationError as error:
			self.error( u"Python Compilation Error: {msg}".format(
							msg  = error.message ) )

			return COMPILATION_FAILED


	def __execute_script( self, env, safe ):
		if not self.code:
			return EXECUTION_SUCCESS

		if not self.cache:
		#	if self.__compile( env ) == COMPILATION_FAILED:
			return COMPILATION_FAILED

		self.info( u"VScript initializing" )

		status = EXECUTION_SUCCESS
		#self.info( "Exec env:" +str(dict( env )))
		try:
			execute( self.cache, self.debuginfo, env, safe = safe )

		except VScriptExecutionError as error:
			self.parse_error(error, "VScript Execution Error")
			status = EXECUTION_FAILED

		except StopExecutionError as error:
			status = EXECUTION_SUCCESS

		except PythonExecutionError as error:
			from vdom_trace import Trace
			msg = [ u"Python Execution Error:" ]
			msg.extend( Trace.print_traceback() )
			msg.append( u"Exception: {0}".format( error.message ) )
			self.error( u" --> ".join( msg ) )
			status = EXECUTION_FAILED

		self.info( u"VScript executed" )
		return status


	def info( self, msg ):
		self.logger.info(msg)


	def error( self, msg ):
		self.logger.error(msg)


	def clear_log( self ):
		pass


	def activate_timer( self, timer_name ):
		engine.activate_timer( "{0}:{1}".format( self.namespace, timer_name ).lower(), True )


	def deactivate_timer( self, timer_name ):
		engine.activate_timer( "{0}:{1}".format( self.namespace, timer_name ).lower(), False )


	def get_timer_by_name ( self, timer_name ):
		return engine.get_timer_by_name( "{0}:{1}".format( self.namespace, timer_name ).lower() )



class InvokeDispatcher( object ):

	def __init__( self ):
		self.macros 		= None
		self.xmldialog 		= None
		self.vdomdynobj 	= None
		self.page			= None
		self.growl 			= None
		self.env			= []
		self.current_page 	= None
		self.no_action 		= False

	def add_env_var( self, name, value ):
		self.env.append( ( name, value ) )

	def run( self ):

		from VEE_events import VEE_ButtonEvent

		dispatcher = engine.get_dispatcher_by_event( VEE_ButtonEvent( self.macros.namespace, self.macros.guid ) )
		if not dispatcher:
			#self.growl.action("show", ["Error", "No such macros %s:%s" % ( self.macros.namespace, self.macros.guid ) ] )
			self.growl.action("show", ["Error", "No such macros" ] )
			return

		session_dictionary 	= VEE_std_lib.v_session_dictionary( self.macros.namespace )
		growl = VEE_std_lib.v_growl()
		args = request.arguments
		xml_dialog 					= VEE_std_lib.v_xmldialog()
		xml_dialog.container_guid 	= self.xmldialog.id
		xml_dialog.arguments 		= { k : args.get( k ) for k in args }
		xml_dialog.macros_id		= self.macros.guid

		vdom_dyn_obj = None
		if self.vdomdynobj:
			self.vdomdynobj.visible = "1"
			vdom_dyn_obj = VEE_std_lib.v_dynamicvdom(self.vdomdynobj)

		if self.current_page is not None:
			self.add_env_var( "v_page_status", self.current_page )
			self.add_env_var( "v_currentpage", self.current_page )

		result = dispatcher( event 		= None,
							 env_mask 	= 0b111,
							 custom_env = (
											(	"v_xml_dialog"	, 		xml_dialog			), #obsolete
											( 	"v_xmldialog"	,		xml_dialog			),
											( 	"v_sessiondictionary",	session_dictionary 	),
											(	"v_showgrowl"		, 	growl				),
											(	"v_dynamicvdom",		vdom_dyn_obj 		),
#											(	"v_eac",                promail_wrappers.v_EAC),
										) + tuple( self.env ),
							safe = False
									)
		if self.vdomdynobj:
			self.vdomdynobj.vdomxml = ""
			self.vdomdynobj.vdomactions = ""
			self.vdomdynobj.visible = "0"

		if result == EXECUTION_SUCCESS:

			if self.current_page is not None and self.current_page.redirect_url:
				if self.no_action:
					response.redirect( self.current_page.redirect_url )
				else:
					self.page.action( "goTo", [ self.current_page.redirect_url ] )

			else:
				if growl.message and growl.title:
					if self.no_action:
						self.growl.title = growl.title
						self.growl.text  = growl.message
						self.growl.active = "1"

					else:
						self.growl.action( "show", [ growl.title, growl.message ] )

				if not self.no_action and xml_dialog.actions:
					for action_data in xml_dialog.actions:
						self.xmldialog.action('executeCallback', action_data)

				if xml_dialog.xml:
					if self.no_action:
						self.xmldialog.width = xml_dialog.width
						self.xmldialog.height = xml_dialog.height
						self.xmldialog.xmldata = xml_dialog.xml
						self.xmldialog.show = "1"

					else:
						self.xmldialog.action( "show", [] )
						self.xmldialog.action( "resizeTo", [ xml_dialog.width, xml_dialog.height ] )
						self.xmldialog.action( "loadData", [ xml_dialog.xml ] )

				elif not xml_dialog.visible:
					self.xmldialog.action( "hide", [] )

		elif result == COMPILATION_FAILED:
			self.growl.action("show", ["Compilation error", "Please, check macros code"])

		elif result == EXECUTION_FAILED:
			self.growl.action("show", ["Execution error", "Please, check macros code"])

		else:
			self.growl.action("show", ["Error", "Please, check macros code"])

from VEE_core import engine
