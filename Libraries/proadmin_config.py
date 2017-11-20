import ProAdmin


def create_default_scheme():
	""" insert here creating of application scheme
	"""
	from proadmin_remote_settings import RemoteSettings
	remote = RemoteSettings.get_remote_setting()

	if remote:
		scheme = create_remote_scheme()
	else:
		scheme = create_local_scheme()

	scheme.set_information(application.name)


	# set scheme options
	scheme.set_option( 'api_guid', '5073ff75-da99-44fb-a5d7-e44e5ab28598' ) # API
	scheme.set_option( 'subjects_limit', None ) # subjects limitation

	app_guid = application.id #"26d94c75-ce3d-4019-8475-daf6206db7e3"
	app_type = ProAdmin.ACLObjectType("Application", app_guid)
	app_type.set_access_types({"a": "Admin"})
	scheme.add_aclobjecttype(app_type)

#	# create Mailbox ACL Type
#	mailbox_guid = '24d8c50b-1de8-4c25-995f-eb127d51f154'
#	mailbox_type = ProAdmin.ACLObjectType( 'Mailbox', mailbox_guid )
#	mailbox_type.set_access_types({
#		"d": "Delete",
#		"o": "Owner",
#		"r": "Read",
#		"w": "Write",
#	})
#	scheme.add_aclobjecttype( mailbox_type )

	scheme.register()

	# create admins group and admin user
	app = ProAdmin.application()
	app.create_root_user( password='root' )
	app.create_admins_group()


def create_local_scheme():
	""" create local scheme
	"""
	import os
	import ProAdmin
	from proadmin_db_scheme import DbApplicationScheme
	from proadmin_db_connection import DbConnection

	database_dir = os.path.join(
		application.storage.abs_path('databases'),
		"proadmin"
	)

	try:
		os.stat(database_dir)
	except Exception as ex:
		os.makedirs(database_dir)

	db_path = os.path.join(database_dir, "proadmin.sqlite")
	connection = DbConnection(db_path)

	# create application scheme
	scheme = DbApplicationScheme( application.id, connection )
	return scheme



def create_memory_scheme():
	""" create local scheme memory
	"""
	import ProAdmin
	from proadmin_db_scheme import DbApplicationScheme
	from proadmin_db_connection import DbConnection

	connection = DbConnection()

	# create application scheme
	scheme = DbApplicationScheme( application.id, connection )
	return scheme



def create_remote_scheme():
	""" insert here creating of application scheme
	"""
	import ProAdmin
	from vdom_remote_api import VDOMService
	from md5 import md5
	from proadmin_remote_sync import RemoteSync

	from proadmin_remote_application_scheme import RemoteApplicationScheme
	from proadmin_db_connection import DbConnection

	from class_remote_settings import RemoteSettings

	# create connection to ProAdmin
	remote = RemoteSettings.get_remote_setting()

	server 		= remote.server
	login		= remote.login
	password	= md5( remote.password ).hexdigest()
	app_id		= '491d4c93-4089-4517-93d3-82326298da44'

	# create ldap connection


	import os

	db_path = application.storage.abs_path('test_db.sqlite')
	if not os.path.exists(application.storage.abs_path('')):
		os.makedirs(application.storage.abs_path(''))
	connection = DbConnection(db_path)


	try:
		service = VDOMService( server, login, password, app_id ).open_session()

		# create application scheme
		scheme = RemoteApplicationScheme( application.id, connection )
		scheme.set_sync_service( service )

	except Exception,ex:
		RemoteSettings.delete()
		scheme = create_local_scheme()

	return scheme
