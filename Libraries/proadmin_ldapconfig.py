

CONFIG_IDs = {
	'active_directory' 		: '-1',
	'vdombox.ru' 			: '-2',
	'local'					: '0',
	'create new config..' 	: '-3'
}


class LDAPConfig( object ):
	def __init__( self, attributes = {}, config = '' ):
		self.id = CONFIG_IDs.get( config, '' )
		self.name = config
		if config and not attributes:
			self.attributes = self.create_config( config = config ).attributes
		else:
			self.attributes = attributes

	@classmethod
	def create_config( self, config = 'local' ):
		""" config can be 'local', 'vdombox.ru', 'active_directory' """
		attributes = {
				"first_name"		: "",
				"last_name"			: "",
				"email"				: "",
				"phone"				: "",
				"notification_email": "",
				"cell_phone"		: "",
				"country"			: "",
				"keywords"			: "",
				"password"			: "",
				"user_dn"			: "",
				"group_dn"			: "",
				"user_guid"			: "",
				"group_guid"		: "",
				"base_dn"			: "",
				"groups_in_user"	: '',
				"users_in_group"	: "",
				"user_class"		: [''],
				"group_class"		: [''],
				"group_name"		: '',
				}

		if config == 'local':
			attributes = {
				"first_name"		: "givenName",
				"last_name"			: "sn",
				"email"				: "uid",
				"phone"				: "telephoneNumber",
				"notification_email": "mail",
				"cell_phone"		: "mobile",
				"country"			: "homePostalAddress",
				"keywords"			: "description",
				"password"			: "userPassword",
				"user_dn"			: "ou=users,ou=%s" % application.id,
				"group_dn"			: "ou=users,ou=%s" % application.id,
				"user_guid"			: "cn",
				"group_guid"		: "cn",
				"base_dn"			: "dc=vdombox,dc=local",
				"groups_in_user"	: '',
				"users_in_group"	: "member",
				"user_class"		: [ 'top', 'person', 'organizationalPerson', 'inetOrgPerson' ],
				"group_class"		: [ 'groupOfNames' ],
				"crypt"				: 'md5',
				"group_name"		: 'o',
				}

		elif config == 'vdombox.ru':
			attributes = {
				"first_name"		: "cn",
				"last_name"			: "sn",
				"email"				: "uid",
				"phone"				: "telephoneNumber",
				"password"			: "userPassword",
				"user_dn"			: "ou=developers",
				"group_dn"			: "ou=groups",
				"user_guid"			: "uid",
				"group_guid"		: "cn",
				"group_name"		: "cn",
				"base_dn"			: "dc=vdombox,dc=ru",
				"groups_in_user"	: '',
				"users_in_group"	: "member",
				"user_class"		: [ 'top', 'person', 'organizationalPerson', 'inetOrgPerson' ],
				"group_class"		: [ 'groupOfNames' ],
				"crypt"				: 'base64_sha',
				}

		elif config == 'active_directory':
			attributes = {
				"first_name"		: "givenName",
				"last_name"			: "sn",
				"email"				: "sAMAccountName",
				"phone"				: "telephoneNumber",
				# "password"			: "userPassword",
				# "user_dn"			: "cn=Users",
				# "group_dn"			: "cn=Groups",
				"user_guid"			: "cn",
				"group_guid"		: "cn",
				"group_name"		: "cn",
				# "base_dn"			: "dc=ad,dc=vdombox,dc=local",
				"groups_in_user"	: "",
				"users_in_group"	: "member",
				"user_class"		: [ "User" ],
				"group_class"		: [ "Group" ],
				"crypt"				: "md5",
				"notification_email": "mail",
				"keywords"			: "description",
				"country"			: "co",
				"cell_phone"		: "mobile",
			}

		return LDAPConfig( attributes = attributes, config = config )



	def __getitem__( self, key ):
		return self.attributes.get( key, '' )

	def __setitem__( self, key, value ):
		self.attributes[ key ] = value

	def __delitem__( self, key ):
		if key in self.attributes:
			del self.attributes[ key ]



	def get_attribute( self, attribute_name, default = '' ):
		return self.attributes.get( attribute_name, default )

	def add_attribute( self, name, value ):
		self.attributes[ name ] = value

	def set_attribute( self, name, value ):
		self.attributes[ name ] = value



	def get_login( self, username ):
		if not username: return ''

		uid = self.get_attribute( 'user_guid' )
		user_dn = self.get_attribute( 'user_dn' )
		base_dn = self.get_attribute( 'base_dn' )

		dn = "%(uid)s=%(login)s,%(user_dn)s,%(base_dn)s" % {
			"uid"		: uid,
			"login"		: username,
			"user_dn"	: user_dn,
			"base_dn"	: base_dn,
		}

		return dn


	def get_group_dn( self, guid, base_dn ):
		if not guid: return ''

		guid_attr = self.get_attribute( 'group_guid' )
		group_dn = self.get_attribute( 'group_dn' )

		dn = "%(guid_attr)s=%(guid)s,%(group_dn)s,%(base_dn)s" % {
			"guid_attr"	: guid_attr,
			"guid"		: guid,
			"group_dn"	: group_dn,
			"base_dn"	: base_dn,
		}

		return dn


	def get_user_dn( self, guid, base_dn ):
		if not guid: return ''

		guid_attr = self.get_attribute( 'user_guid' )
		user_dn = self.get_attribute( 'user_dn' )

		dn = "%(guid_attr)s=%(guid)s,%(user_dn)s,%(base_dn)s" % {
			"guid_attr"	: guid_attr,
			"guid"		: guid,
			"user_dn"	: user_dn,
			"base_dn"	: base_dn,
		}

		return dn


	def get_user_guid( self ):
		guid = self.attributes.get( 'user_guid' )
		for k, v in self.attributes.items():
			if v == guid:
				return k
		return 'dn'


	def get_group_guid( self ):
		guid = self.attributes.get( 'group_guid' )
		for k, v in self.attributes.items():
			if v == guid:
				return k
		return 'dn'



	################################################################
########	db_config
	################################################################



	@classmethod
	def get_by_id( self, id ):
		from class_db import Database

		for config_name, config_id in CONFIG_IDs.items():
			if str( config_id ) == str( id ):
				return LDAPConfig( config = config_name )

		query = """
			SELECT
				email,
				phone,
				password,
				group_dn,
				user_dn,
				user_guid,
				group_guid,
				base_dn,
				groups_in_user,
				users_in_group,
				user_class,
				group_class,
				group_name,
				first_name,
				last_name,
				config_name,
				id
			FROM subject_config WHERE id = ?
			"""
		values = (id,)

		db_row = Database.maindb().fetch_one( query, values )
		return LDAPConfig().__fill_from_row( db_row ) if db_row else None


	def __fill_from_row( self, row ):
		from class_db import Database

		# define order of attributes
		keys = [
			'email',
			'phone',
			'password',
			'group_dn',
			'user_dn',
			'user_guid',
			'group_guid',
			'base_dn',
			'groups_in_user',
			'users_in_group',
			'user_class',
			'group_class',
			'group_name',
			'first_name',
			'last_name'
		]

		# fill attrbutes
		self.attributes.clear()

		for i in range( len(keys) ):
			key = keys[i]
			value = row[i] if row[i] != u'NULL' else u''

			if key in [ 'group_class', 'user_class' ]:
				value = [ value ]

			self[ key ] = value

		self.name 	= row[15]
		self.id 	= row[16]

		return self


	def save( self ):
		id = self._exist()
		if not id:
			id = self._insert()
		else:
			self._update( id )
		return id


	def _insert( self ):
		from class_db import Database

		query = """
			INSERT INTO subject_config
				(email,
				phone,
				password,
				group_dn,
				user_dn,
				user_guid,
				group_guid,
				group_name,
				base_dn,
				groups_in_user,
				users_in_group,
				user_class,
				group_class,
				first_name,
				last_name,
				config_name)
			VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
			"""

		values = (
			self[ 'email' ],
			self[ 'phone' ],
			self[ 'password' ],
			self[ 'group_dn' ],
			self[ 'user_dn' ],
			self[ 'user_guid' ],
			self[ 'group_guid' ],
			self[ 'group_name' ],
			self[ 'base_dn' ],
			self[ 'groups_in_user' ],
			self[ 'users_in_group' ],
			self[ 'user_class' ][-1],
			self[ 'group_class' ][-1],
			self[ 'first_name' ],
			self[ 'last_name' ],
			self.name,
		)

		self.id = Database.maindb().commit( query, values )
		return id


	def _update( self, id ):
		from class_db import Database

		if self.id in CONFIG_IDs.values():
			return
		self.id = id
		query = """
			UPDATE subject_config SET email = ?,
				phone = ?,
				password = ?,
				group_dn = ?,
				user_dn = ?,
				user_guid = ?,
				group_guid = ?,
				group_name = ?,
				base_dn = ?,
				groups_in_user = ?,
				users_in_group = ?,
				user_class = ?,
				group_class = ?,
				first_name = ?,
				last_name = ?,
				config_name = ?
			WHERE id = ?"""

		values = (
			self[ 'email' ],
			self[ 'phone' ],
			self[ 'password' ],
			self[ 'group_dn' ],
			self[ 'user_dn' ],
			self[ 'user_guid' ],
			self[ 'group_guid' ],
			self[ 'group_name' ],
			self[ 'base_dn' ],
			self[ 'groups_in_user' ],
			self[ 'users_in_group' ],
			self[ 'user_class' ][-1],
			self[ 'group_class' ][-1],
			self[ 'first_name' ],
			self[ 'last_name' ],
			self.name,
			self.id,
		)

		Database.maindb().commit( query, values )



	def _exist( self ):
		from class_db import Database

		if self.id: return self.id
		if self.name in CONFIG_IDs:	return CONFIG_IDs[ name ]

		query = """
			SELECT id
			FROM subject_config
			WHERE
				user_dn = ?
				AND group_dn = ?
				AND user_guid = ?
				AND group_guid = ?
				AND users_in_group = ?
				AND groups_in_user = ?
			"""

		values = (
			self[ 'user_dn' ],
			self[ 'group_dn' ],
			self[ 'user_guid' ],
			self[ 'group_guid' ],
			self.get_attribute( 'users_in_group', 'NULL' ),
			self.get_attribute( 'groups_in_user', 'NULL' ),
		)

		id = Database.maindb().fetch_one( query, values )
		id = id[0] if id else None

		return id



	def delete( self ):
		from class_db import Database

		if self.id in CONFIG_IDs:
			return
		query = """DELETE FROM subject_config WHERE id = ?"""
		values = ( self.id, )
		Database.maindb().commit( query, values )



	@classmethod
	def get_name_list( self ):
		from class_db import Database

		rows = Database.maindb().fetch_all("""SELECT id, config_name FROM subject_config""")

		result = [ [ id, name ] for name, id in CONFIG_IDs.iteritems() ]
		result.reverse()

		for row in rows:
			result.append( [row[0], row[1]] )

		return result
