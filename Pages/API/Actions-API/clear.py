import managers
import ProAdmin
from class_db import Database
from class_errors import AccessDeniedError
import json
import clear

def is_admin():
	# get server's user
	user = managers.request_manager.current.session().user
	return user == u'root'


def send_response( message ):
	session[ 'response' ] =  json.dumps( message ) #added json.dumps() 10.01.2013 Nikita


def clear_all():
	clear.clear_all()

#	# clear LDAP base
#	ProAdmin.scheme().delete()
#
#	# delete all application storage
#	application.storage.rmtree('.')
#
#	# clear database
#	Database.maindb().clean()
#	Database.maindb().commit( 'VACUUM' )
#
#	Database.macrosdb().clean()
#	Database.macrosdb().commit( 'VACUUM' )
#
#	# clear all listeners and timers in VEE_core
#	engine.clear_all()


try:
	if not is_admin():
		raise AccessDeniedError()

	clear_all()
	send_response( ['success'] ) #added [] 10.01.2013 Nikita

except AccessDeniedError:
	send_response( ['error', 'premission_denied'] ) #added ['error', ...] 10.01.2013 Nikita

except Exception:
	send_response( ['error', 'unkonwn error'] ) #added [..., 'unknown error'] 10.01.2013 Nikita
