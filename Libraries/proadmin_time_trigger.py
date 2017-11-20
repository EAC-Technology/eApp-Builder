from utils.threads import VDOM_thread


class BackgroundThread( VDOM_thread ):
	def __init__( self, app_id=None ):
		VDOM_thread.__init__( self, name = 'time trigger' )

		# sometimes need to set applicatino id
		self.app_id = app_id

		# is daemon thread
		self.daemon = True


	def define_application( self ):
		try:
			if self.app_id:
				application.set_app_id( self.app_id )
		except:
			pass



class ProAdminTimeTrigger( BackgroundThread ):
	# default wait timeout
	DEFAULT_TIMEOUT = 10

	def __init__( self ):
		BackgroundThread.__init__( self, app_id = application.id )

		self.procedure = None


	def work( self ):
		try:
			self.save_thread()
			return self.execute()
		except:
			try:
				return ProAdminTimeTrigger.DEFAULT_TIMEOUT
			except:
				self.stop()


	def execute( self ):
		timeout = None
		self.define_application()

		if self.procedure:
			import ProAdmin
			timeout = self.procedure( ProAdmin.scheme() )

		return timeout if timeout else ProAdminTimeTrigger.DEFAULT_TIMEOUT


	def save_thread( self ):
		try:
			import ProAdmin
			ProAdmin.sync_thread = self
		except:
			pass


	def set_action( self, procedure ):
		self.procedure = procedure

	def unset_action( self ):
		self.procedure = None

