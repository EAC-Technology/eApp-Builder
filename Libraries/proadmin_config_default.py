from md5 import md5
import ProAdmin
from class_external_settings import ExternalSettings
from proadmin_ldap_connection import LDAPConnection
from proadmin_ldapconfig import LDAPConfig

def create_default_scheme():
	""" insert here creating of application scheme
	"""
	external_settings = ExternalSettings.get_last()

	scheme = None

	if external_settings:
		scheme = create_external_scheme() if external_settings.active == 'active' else None

	if not scheme:
		scheme = create_local_scheme()

	scheme.set_information( application.name )


	app_guid = application.id
	app_type = ProAdmin.ACLObjectType( "Application", app_guid )
	app_type.set_access_types( { 'a': 'Admin' } )
	scheme.add_aclobjecttype( app_type )

	app_guid =  "0190754a-0843-4138-9b07-9a055c50304f"
	app_type = ProAdmin.ACLObjectType( "RemoteApplication", app_guid )
	app_type.set_access_types( { "a": "Admin", 'r': "Read", 'w': 'Write' } )
	scheme.add_aclobjecttype( app_type )

	# set API guid
	scheme.set_api_guid( '19a67ddc-a792-41fd-bbee-b5190126b6dc' )

	scheme.register( make_default=True )
	app = ProAdmin.application()

	# create admin user and admin group
	root = app.create_root_user()
	admin = app.create_admins_group()


def create_local_scheme():
	server = '127.0.0.1'
	login = 'cn=admin,dc=vdombox,dc=local'
	password = 'passwd'

	ldapconnection = LDAPConnection()
	ldapconnection.bind(  server, login, password )

	scheme = ProAdmin.local_scheme( application.id, ldapconnection )
	base_dn = 'dc=vdombox,dc=local'
	scheme.set_option( 'base_dn', base_dn )
	scheme.set_option( 'root_user', 'root' )
	scheme.set_option( 'admin_group', 'Administrators' )

	return scheme



def create_external_scheme():
	import ProAdmin
	import re
	from proadmin_ldap_connection import LDAPConnection
	from proadmin_external_settings import ProAdminSchemeConfig
	from proadmin_ldapconfig import LDAPConfig

	active_config = ProAdminSchemeConfig.get_active()
	connection_settings= ProAdminSchemeConfig.get_connection_settings()

	active_config[ 'base_dn' ] = connection_settings[ 'base_dn' ]

	server = connection_settings[ 'server' ]
	login =  connection_settings[ 'login'  ]
	password = connection_settings[ 'password' ]

	active_config = LDAPConfig( active_config.attributes, active_config.name )

	# try to connect to active directory by some dn
	def try_bind( dn ):
		return LDAPConnection.try_bind( server, dn, password )

	# if login cantains '=' and ',' symbols - it's some dn string
	if re.search('[=,]', login):
		dn = login
	else:
		user_dn = 'cn=Users'
		dn = "%(uid)s=%(login)s,%(user_dn)s,%(base_dn)s" % {
					"uid"		: active_config.get_attribute( 'user_guid' ),
					"login"		: login,
					"user_dn"	: user_dn,
					"base_dn"	: active_config.get_attribute( 'base_dn' ),
		}

	if not try_bind( dn ):
		dn += ',' + active_config.get_attribute( 'base_dn' )

	user_connection = LDAPConnection()
	user_connection.bind( server, dn, password )

	server = '127.0.0.1'
	login = 'cn=admin,dc=vdombox,dc=local'
	password = 'passwd'

	local_connection = LDAPConnection()
	local_connection.bind(  server, login, password )

	scheme = ProAdmin.external_scheme( application.id, local_connection, user_connection, active_config )
	scheme.set_option( 'base_dn', connection_settings[ 'base_dn' ] )
	scheme.set_option( 'root_user', connection_settings[ 'root_user' ] )
	return scheme

