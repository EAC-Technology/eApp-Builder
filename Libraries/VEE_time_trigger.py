from utils.threads import VDOM_thread


appId = application.id

class engineTimeTrigger( VDOM_thread ):
	# default wait timeout
	DEFAULT_TIMEOUT = 10

	def __init__( self ):
		VDOM_thread.__init__( self )


	def work( self ):
		import VEE_core
#		VEE_core.engine.engine_logger.debug("Engine thread work...")
		try:
			#debug("------------>>>> Trying to start engine: ")
			application.set_app_id( appId )
			self.save_thread()
			return VEE_core.engine.process_queue()
		except Exception as e:
#			from vdom_trace import Trace
#			VEE_core.engine.log("@@@@@@@@@Error while vscript execution." )
#			VEE_core.engine.log( Trace.exception_trace() )

			try:
				VEE_core.engine.info( str( e ) )
			except: pass
			#debug("------------>>>> Exception: %s"%e)
			try:
				return engineTimeTrigger.DEFAULT_TIMEOUT
			except:
				self.stop()


	def save_thread( self ):
		try:
			import VEE_core
			#VEE_core.VEE_core = self
			VEE_core.queue_thread = self
		except:
			pass
