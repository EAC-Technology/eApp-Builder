import ProAdmin
from class_db import Database
from VEE_core import engine
import managers
import clear


def clear_all():
	clear.clear_all()

	#clear web-dav cache
	#managers.webdav_manager.clear()

#	# clear database
#	Database.maindb().clean()
#	Database.maindb().commit( 'VACUUM' )
#
#	Database.macrosdb().clean()
#	Database.macrosdb().commit( 'VACUUM' )
#
#	# clear ProAdmin scheme
#	ProAdmin.scheme().delete()
#
#	# clear application storage
#	application.storage.rmtree('.')
#
#	# clear all listeners and timers in VEE_core
#	engine.clear_all()



try:

	# check admin rights
	user = ProAdmin.current_user()
	if not user:
		raise Exception()

	if not ProAdmin.application().rules( user, 'a' ):
		raise Exception()

	# check entered password
	password = request.arguments.get( 'password', '' )

	if not user.check_password( password ):
		raise Exception()

	clear_all()
	self.accept_dialog.text_warning.value = 'Clearing complete'

except:
	self.action( 'goTo', ['/login'] )
