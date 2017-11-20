import uuid
import base64
import json
from md5 import md5
from proadmin_subject import User




_pack_scheme = ['guid',
			'email',
			'first_name',
			'last_name',
			'phone',
			'password_hash',
			'notification_email',
			'cell_phone',
			'country',
			'keywords_string',
			'options_string',
			]

class DbUser( User ):


	@classmethod
	def get_users( self, scheme, email = None, guid = None ):
		global _pack_scheme

		filter_dict = {}
		if email: filter_dict["email"] = email
		if guid: filter_dict["guid"] = guid

		raw_result = scheme.connection.select_cmd('proadmin_user', _pack_scheme, filter_dict)
		return [DbUser(scheme).init_from_db_tuple(db_tuple) for db_tuple in raw_result]



	@classmethod
	def get_in_group( self, scheme, group ):
		raw_result = scheme.connection.fetch_all(
			'''SELECT %s 
			FROM proadmin_user 
			JOIN user_in_group ON user_guid = guid
			WHERE group_guid = ? ''' % (', '.join(_pack_scheme),), [group.guid])

		return [DbUser(scheme).init_from_db_tuple(db_tuple) for db_tuple in raw_result]


	def __init__( self, scheme ):
		User.__init__( self, scheme )
		self.connection = scheme.connection

		self._guid = str(uuid.uuid4())
		self.keywords_string = ''
		
		self.options_string = ''
		self.__options = None


	def init_from_db_tuple(self, db_tuple):
		global _pack_scheme
		for k, v in zip(_pack_scheme, db_tuple):
			setattr(self, k, v)
		return self



	def _packed_list(self, pscheme = None):
		global _pack_scheme
		if not pscheme: pscheme = _pack_scheme
		return [getattr(self, attr) for attr in pscheme]

	def _packed_dict(self, pscheme = None):
		global _pack_scheme
		if not pscheme: pscheme = _pack_scheme
		return dict([(attr, getattr(self, attr)) for attr in pscheme])
		
	
	def save( self ):
		global _pack_scheme

		self.options_string = json.dumps(self.options)

		exists = len(self.connection.select_cmd('proadmin_user', _pack_scheme, {'guid': self.guid})) > 0

		if exists:
			self.connection.update_cmd('proadmin_user', self._packed_dict(), {'guid': self.guid} )
		else:
			self.connection.insert_cmd('proadmin_user', _pack_scheme, self._packed_list())
		return self

	
	def force_delete( self, force=True ):
		self.connection.delete_cmd( 'user_in_group', {"user_guid": self.guid})
		self.connection.delete_cmd( 'rule', {"subject_guid": self.guid})
		self.connection.delete_cmd( 'proadmin_user', {"guid": self.guid})



	def get_groups( self ):
		from proadmin_db_group import DbGroup
		if not hasattr(self, "__groups"):
			self.__groups = User.get_groups(self) + DbGroup.get_user_groups(self.scheme, self)
		return self.__groups



	def _get_hash(self, value):
		return base64.b64encode( md5( value.encode('utf8') + self.guid ).digest() )

	def remove_group(self, group):
		group.remove_user(self)
		

	def add_group(self, group):
		group.add_user(self)
		

	@property
	def password_hash( self ):
		return self._password

	@password_hash.setter
	def password_hash( self, value ):
		self._password = value 
		
	def set_password_hash( self, value ):
		self.password_hash = value


	@property
	def password( self ):
		return self._password

	@password.setter
	def password( self, value ):
		if not value: return ""
		self._password = self._get_hash( value )
	
	def check_local_password( self, password ):
		return self.password == self._get_hash( password )


	@property
	def keywords(self):
		return self.keywords_string.split(',')

	@keywords.setter
	def keywords(self, value):
		self.keywords_string = ",".join(value)


	@property
	def options(self):
		if self.__options is None:
			self.__options = json.loads(self.options_string) if self.options_string else {}
		return self.__options

	@options.setter
	def options(self, value):
		self.__options = value
		

	def __repr__(self):
		return str(self.email)