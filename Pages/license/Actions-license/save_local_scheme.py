import ProAdmin
from class_remote_settings import RemoteSettings

class EmptyPasswordError( Exception ):
	def __init__( self ):
		Exception.__init__( self, 'Password must be not empty' )

password = request.arguments.get( "formpassword", '' )
confirm = request.arguments.get( "formpassword_confirm", "" )
try:
	if not password:
		raise EmptyPasswordError()
	if password == confirm:
		user = ProAdmin.application().get_users( email="root" )
		if user:
			user[0].password = password
			user[0].save()
			from class_license import License
			License().confirmed = "True"


			if RemoteSettings.get_remote_setting():
				RemoteSettings.delete()

			ProAdmin.unregister_default_scheme()
			ProAdmin.scheme()
			ProAdmin.logoff()
			self.action("goTo",["/logoff"])
	else:
		self.growl.action("show",[ 'Warning', "The passwords you entered did not match." ])

except EmptyPasswordError as ex:
	self.growl.action("show",[ 'Error', ex.message ])

except Exception as ex:
	self.growl.action("show",[ 'Error', ex.message ])
