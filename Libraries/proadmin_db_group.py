from proadmin_subject import Group
import uuid


_pack_scheme = ['guid', 'name']

class DbGroup( Group ):

	@classmethod
	def get_groups( self, scheme, name = None, guid = None ):
		global _pack_scheme

		filter_dict = {}
		if name: filter_dict["name"] = name
		if guid: filter_dict["guid"] = guid

		raw_result = scheme.connection.select_cmd('proadmin_group', _pack_scheme, filter_dict)
		return Group.get_groups( scheme, name, guid ) + [DbGroup(scheme).init_from_db_tuple(db_tuple) for db_tuple in raw_result]



	@classmethod
	def get_user_groups( self, scheme, user ):
		raw_result = scheme.connection.fetch_all(
			'''SELECT %s 
			FROM proadmin_group 
			JOIN user_in_group ON group_guid = guid
			WHERE user_guid = ? ''' % (', '.join(_pack_scheme),), [user.guid])

		return [DbGroup(scheme).init_from_db_tuple(db_tuple) for db_tuple in raw_result]



	def delete(self):
		self.force_delete()
	
	def force_delete( self, force=True ):
		self.connection.delete_cmd( 'user_in_group', {"group_guid": self.guid})
		self.connection.delete_cmd( 'rule', {"subject_guid": self.guid})
		self.connection.delete_cmd( 'proadmin_group', {"guid": self.guid})


	def __init__( self, scheme ):
		Group.__init__( self, scheme )
		self.connection = scheme.connection

		self._guid = str(uuid.uuid4())
		self.user_guid_list = None


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

		exists = len(self.connection.select_cmd('proadmin_group', _pack_scheme, {'guid': self.guid})) > 0

		if exists:
			self.connection.update_cmd('proadmin_group', self._packed_dict(), {'guid': self.guid} )
		else:
			self.connection.insert_cmd('proadmin_group', _pack_scheme, self._packed_list())


		if self.user_guid_list is not None:
			self.connection.delete_cmd( 'user_in_group', {'group_guid': self.guid} )
			for user_guid in self.user_guid_list:
				self.connection.insert_cmd( 'user_in_group', ['user_guid', 'group_guid'], (user_guid, self.guid) )


		return self



	def add_user(self, user):
		if self.user_guid_list is None: self.get_users()
		if user.guid not in self.user_guid_list:
			self.user_guid_list.append(user.guid)
			self.save()
		
	def remove_user(self, user):
		if self.user_guid_list is None: self.get_users()
		if user.guid in self.user_guid_list:
			self.user_guid_list.remove(user.guid)
			self.save()

	def get_users( self ):
		from proadmin_db_user import DbUser
		myusers = DbUser.get_in_group(self.scheme, self)
		self.user_guid_list = [user.guid for user in myusers]
		return myusers



	def __repr__(self):
		return str(self.name)
