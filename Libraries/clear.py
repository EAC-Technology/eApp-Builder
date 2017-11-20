import ProAdmin
from class_db import Database
from VEE_core import engine


def clear_all():

	# clear database
	Database.maindb().clean()
	Database.maindb().commit( 'VACUUM' )

	Database.macrosdb().clean()
	Database.macrosdb().commit( 'VACUUM' )

	# clear ProAdmin scheme
	ProAdmin.scheme().delete()

	# clear application storage
	application.storage.rmtree('.')

	# clear all listeners and timers in VEE_core
	engine.clear_all()
