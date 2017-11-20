import threading
from vdom_remote_api import VDOMService, VDOMServiceCallError
from md5 import md5


from proadmin_remote_sync import APIFormat


class APIError( Exception ):
	def __init__( self, message, conn=None ):
		Exception.__init__( self, message )
		
		# save last error message in connection
		if conn:
			conn.last_error = message




class APIConnection:
	""" class singleton for remote api routines
	"""

	__local	= threading.local()

	def __init__( self, vdom_service, cont_id, app_id=None ):
		self.service		= vdom_service
		self.cont_id		= cont_id
		self.app_id			= app_id

		self.last_error		= None


	def set_application_id( self, id ):
		self.app_id = id



	def call( self, action_name, params=None ):
		if not self.app_id:
			raise Exception( 'Application ID not defined' )

		# generate request data
		xml_data = APIFormat.request( self.app_id, params )

		# call remote action
		try:
			response_xml = self.service.call( self.cont_id, action_name, xml_data )
		except VDOMServiceCallError:
			self.service.open_session()
			response_xml = self.service.call( self.cont_id, action_name, xml_data )

		# parse response
		status, result = APIFormat.parse_response( response_xml )

		self.last_error = None

		if not status:
			raise APIError( 'Invalid call response', self )

		if status == 'success':
			return result
		else:
			raise APIError( result, self )


	def clone( self ):
		""" create copy of this connection """
		return self.create_copy( self )


	@classmethod
	def create_copy( self, connection ):
		""" create copy (another instance) of APIConnection object
		"""
		return APIConnection( connection.service, connection.cont_id, connection.app_id )
		
		
		
		
		
		
