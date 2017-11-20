from utils.threads import VDOM_thread


appId = application.id


class compilerTimeTrigger( VDOM_thread ):
	# default wait timeout
	DEFAULT_TIMEOUT = 10.0

	def __init__( self ):
		VDOM_thread.__init__( self )


	def work( self ):
		import VEE_core
#		VEE_core.engine.engine_logger.debug("Compiler thread work...")
		try:
			application.set_app_id( appId )
			self.save_thread()
			return VEE_core.engine.do_compile()
		except Exception as e:
#			from vdom_trace import Trace

			VEE_core.engine.engine_logger.exception("@@@@@@@@@Error while vscript compilation." )
			VEE_core.engine.engine_logger.info( Trace.exception_trace() )

#			try:
#				VEE_core.engine.engine_logger..info( str( e ) )
#			except: pass
			try:
				return self.DEFAULT_TIMEOUT
			except:
				self.stop()


	def save_thread( self ):
		try:
			import VEE_core
			VEE_core.compiler_thread = self
		except:
			pass
