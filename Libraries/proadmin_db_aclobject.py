from proadmin_rule import Rule

import uuid as uuid
import cgi


_pack_scheme = ['object_type', 'guid', 'name', 'parent_guid', 'is_dirty']

class DbACLObject( object ):

	def __init__( self, db_tuple, scheme, is_new = None ): 
		#is_new = None meaning Unknown state, need db check
		self.init_from_tuple(db_tuple)

		self.scheme	= scheme
		self.connection = scheme.connection

		self.is_new = is_new

		self._rules_cache = [] if self.is_new else None



	@classmethod
	def get_aclobjects( self, scheme, guid = None ):
		filter_dict = {}
		if guid: filter_dict["guid"] = guid

		raw_result = scheme.connection.select_cmd('aclobject', _pack_scheme, filter_dict)
		return [DbACLObject(child_tuple, scheme, is_new=False) for child_tuple in raw_result]

	@classmethod
	def get_rules(self, scheme, subject=None, access=None):
		subject_list = self.listify(subject)
		access_list	= self.listify(access)

		subject_guid_list = reduce(lambda a,b: a+b, [s.get_guid_list() for s in subject_list],[])
		guid_list = reduce(lambda a,b: a+b, [s.get_guid_list() for s in subject_list],[])
		
		condition2 = { 'subject_guid': [ s_guid for s_guid in subject_guid_list] }
		condition3 = { 'access': access_list }

		where_clause, parameters = scheme.connection.build_complex_where_clause( [condition2, condition3] )
		query = '''SELECT aclobject_guid, subject_guid, access FROM rule WHERE ''' + where_clause
		#print (query)
		result = scheme.connection.fetch_all(query, parameters)
		
		return result
		
	def init_from_tuple(self, db_tuple):
		self._type_guid, self._guid, self._name, self._parent_guid, self.dirty = db_tuple


	def as_tuple(self):
		return (self._type_guid, self._guid, self._name, self._parent_guid, self.dirty)
	

	def is_dirty( self ):
		return self.dirty > 0

	def clear_dirty_bit( self ):
		self.dirty = -1

	def get_type( self ):
		return self._type_guid


	def get_guid( self ):
		return self._guid

	def set_guid( self, guid ):
		self._guid = guid

	def get_name( self ):
		return self._name

	def set_name( self, value ):
		#value = cgi.escape( value )
		self._name = value

	def get_parent( self ):
		obj = self.connection.select_cmd('aclobject', _pack_scheme, {'guid': self._parent_guid} )
		return DbACLObject( obj[0], self.scheme, is_new=False ) if obj else None


	type 	= property( get_type )
	guid 	= property( get_guid, set_guid )
	name 	= property( get_name, set_name )
	parent 	= property( get_parent )


	def refresh( self ):
		self.init_from_tuple( self.connection.select_cmd('aclobject', _pack_scheme, {'guid': self.guid} )[0] )


	def delete( self, parent_dirty=True ):
		# mark dirty-bit in parent object
		if parent_dirty and self.parent:
			self.parent.save()

		self.connection.delete_cmd('rule', {'aclobject_guid': self.guid} )
		self.connection.delete_cmd('aclobject', {'guid': self.guid} )

	def create_child( self, type, name, guid = '' ):
		
		if not guid:
			guid = str( uuid.uuid4() )

		child_tuple = (type, guid, name, self.guid, 1);

		return DbACLObject( child_tuple, self.scheme, is_new=True )




	def get_by_guid( self, guid ):
		""" search ACL object by guid in subtree include this object
		"""
		if not guid:
			return None
		
		if guid == self.guid:
			return self

		objects = self.child_objects( guid=guid, recursive=True )
		return objects[0] if objects else None


	def child_objects(self, guid=None, type=None, name=None, recursive=False):
		""" return list of child objects
		"""
		object_type_list = self.listify(type)
		guid_list = self.listify(guid)
		name_list = self.listify(name)

		condition1 = [ ('parent_guid = ?', self.guid) ]
		condition2 = [ ('object_type = ?', item) for item in object_type_list]
		condition3 = { 'guid': guid_list }
		condition4 = [ ('name = ?', item) for item in name_list]
	
		raw_result = self.connection.select_cmd('aclobject', _pack_scheme, [condition1, condition2, condition3, condition4])

		result = [DbACLObject(child_tuple, self.scheme, is_new=False) for child_tuple in raw_result]
		result.sort( cmp=lambda a,b: cmp(a.name, b.name) )

		
		#recursive query
		if recursive:
			child_results = [child.child_objects(guid, type, name, recursive) for child in self.child_objects()]
			for ch in child_results:
				result += ch

		return result

	@classmethod
	def listify(self, scalar_or_list):
		if scalar_or_list is None: return []

		if isinstance( scalar_or_list, list ) or isinstance( scalar_or_list, tuple ) : return list(scalar_or_list)

		return [scalar_or_list]
		
	def create_rules(self, rule_tuples):
		from proadmin_db_user import DbUser
		from proadmin_db_group import DbGroup
		#TODO: refactor here, very slow
		subject_cache = {}
		aclobject_cache = {}

		result = []
		for aclobject_guid, subject_guid, access in rule_tuples:
			#subject and objects are localy cached not to fetch db every time
			if aclobject_guid not in aclobject_cache:
				aclobject = self if aclobject_guid == self.guid else DbACLObject.get_aclobjects(scheme = self.scheme, guid = aclobject_guid)[0]
				aclobject_cache[aclobject_guid] = aclobject
			else:
				aclobject = aclobject_cache[aclobject_guid]

			if subject_guid not in subject_cache:
				subject = (DbUser.get_users(scheme = self.scheme, guid = subject_guid) or DbGroup.get_groups(scheme = self.scheme, guid = subject_guid))[0]
				subject_cache[subject_guid] = subject
			else:
				subject = subject_cache[subject_guid]


			result.append(Rule(aclobject, subject, access))
		return result

	def rules_cache(self):
		if self._rules_cache is None:
			self._rules_cache = self.create_rules( self.fast_rules(for_myself = True) )
		return self._rules_cache

	def get_rules_tuples( self ):
		return [ (r.subject, r.access) for r in self.rules_cache() ]

	def set_rules_tuples( self, subject_access_list ):
		self._rules_cache = [] #empty cache
		for (s, a) in subject_access_list:
			self.add_rule(s, a)
	
	
		
	def rules( self, subject=None, access=None ):
		subject_list = self.listify(subject)
		access_list = self.listify(access)
		guid_list = reduce(lambda a,b: a+b, [s.get_guid_list() for s in subject_list],[])

		rules = self.rules_cache()
		if subject_list:
			rules = filter( lambda x: x.subject.guid in guid_list, rules)
		if access_list:
			rules = filter( lambda x: x.access in access_list, rules)
		return rules


	def child_rules( self, objecttype=None, subject=None, access=None, recursive=False ):
		return self.create_rules( self.fast_rules(objecttype, subject, access, recursive) )


	def fast_rules( self, objecttype=None, subject=None, access=None, recursive=False, get_empty=False, for_myself=False):
		""" fast implementation for rules retreive. return rule like tuple of guids: (obj, subj, access)
		"""
		objecttype_list = self.listify(objecttype)
		subject_list = self.listify(subject)
		access_list	= self.listify(access)

		subject_guid_list = reduce(lambda a,b: a+b, [s.get_guid_list() for s in subject_list],[])


		condition1 = [ ('aclobject.parent_guid = ?', self.guid) ] if not for_myself else [ ('aclobject_guid = ?', self.guid) ]
		condition2 = { 'subject_guid': [ s_guid for s_guid in subject_guid_list] }
		condition3 = { 'access': access_list }
		condition4 = { 'aclobject.object_type': objecttype_list }

		where_clause, parameters = self.connection.build_complex_where_clause( [condition1, condition2, condition3, condition4] )
		query = '''SELECT aclobject_guid, subject_guid, access 
			FROM rule ''' + 	(''' JOIN aclobject ON rule.aclobject_guid = aclobject.guid''' if not for_myself or objecttype_list else "")	+ ''' WHERE ''' + where_clause
		#print (query)
		result = self.connection.fetch_all(query, parameters)
		
		#recursive query
		if recursive:
			child_results = [child.fast_rules(objecttype, subject, access, recursive, get_empty, for_myself) for child in self.child_objects()]
			for ch in child_results:
				result += ch

		return result
	



	def add_rule( self, subject, access ):
		r = Rule(subject=subject, object=self, access=access)
		if r not in self.rules_cache():
				self._rules_cache.append(r)


	def remove_rule( self, subject, access ):
		self.rules_cache() # ensure lazy-initialize
		self._rules_cache.remove( Rule(subject=subject, object=self, access=access) )


	def force_remove_rule( self, subject, access, force=True ):
		self.remove_rule(subject, access)
		self.connection.delete_cmd('rule', {"aclobject_guid": self.guid, "subject_guid": subject.guid, "access": access})



	def inherit_rules(self):
		rt = self.get_rules_tuples() #save for future

		query = """WITH RECURSIVE child(guid) AS (
			VALUES(?)
			UNION
				SELECT aclobject.guid
				FROM aclobject, child
				WHERE aclobject.parent_guid = child.guid
			) 
			DELETE FROM rule WHERE aclobject_guid in child"""	
		
		self.connection.execute( query, (self.guid,) )

		query = """WITH RECURSIVE child(guid) AS (
			VALUES(?)
			UNION
				SELECT aclobject.guid
				FROM aclobject, child
				WHERE aclobject.parent_guid = child.guid
			)
			INSERT INTO rule (aclobject_guid, subject_guid, access) SELECT child.guid, request_rule.subject, request_rule.access FROM child JOIN ({}) as request_rule""".format(" UNION ".join(["SELECT ? as subject,? as access"]*len(rt)))

		self.connection.execute( query, [self.guid ] + reduce( list.__add__, map(lambda x: [x[0].guid, x[1]], rt), []) )


	def _exist( self ):
		if self.is_new is None: #do not know the state of object, check in DB
			return len(self.connection.select_cmd('aclobject', _pack_scheme, {'guid': self.guid} )) > 0

		return not self.is_new #skip request if is_new is forced

	def save( self ):
		self.dirty = 1 if self.dirty != -1 else 0 #force clean in dirty == -1

		if self._exist():
			self.connection.update_cmd('aclobject', dict(zip(_pack_scheme, self.as_tuple())), {"guid": self.guid}) #todo: update only changed fields
		else:
			self.connection.insert_cmd('aclobject', _pack_scheme, self.as_tuple()  )

		if self._rules_cache is not None:

			self.connection.delete_cmd( 'rule', {"aclobject_guid": self.guid} )
			self.connection.insertmany_cmd( 'rule', ('aclobject_guid', 'subject_guid', 'access'), [(rule.object.guid,rule.subject.guid,rule.access) for rule in self.rules_cache()])

		self.is_new = False
		return self






	@classmethod
	def application( self, name, guid, scheme ):
		application_tuple = ("Application", guid, name, None, 0)

		app = DbACLApplication(application_tuple, scheme)
		if not app._exist():
			app.save()

		return app




	

	def __eq__( self, other ):
		if not other: return False
		return self.as_tuple() == other.as_tuple()

	def __hash__( self ):
		return hash( self.guid )

	def __str__( self ):
		return "DbACLObject: (Type: " + self.type + ", Name: " + self.name + ")"






class DbACLApplication( DbACLObject ):
	
	def get_parent(self):
		return None

	parent = property(get_parent)

	def delete(self):
		import ProAdmin
		super(DbACLApplication, self).delete()
		ProAdmin.unregister_default_scheme()



	def get_subjects( self, guid=None ):
		users = self.get_users( guid=guid )
		groups = self.get_groups( guid=guid )
		return users + groups

	def get_subject( self, guid ):
		result = self.get_subjects( guid=guid )
		return result[0] if result else None


	def create_user(self, email=''):
		""" create new application user
		"""
		users = self.get_users( email = email )
		if users: return users[0]

		user = self.scheme.create_user()
		user.email = email

		return user


	def create_root_user( self, password='root' ):
		""" create root user if not exists. root-is default password
		"""
		root = self.scheme.create_root_user(password)
		if not self.rules( root, 'a' ):
			self.add_rule( root, 'a' )
			self.save()


	def get_users( self, email=None, guid=None ):
		""" get application users
		"""
		return self.scheme.get_users( email = email, guid = guid )

	def get_users_in_group( self, group):
		""" get application users by group guid
		"""
		return self.scheme.get_users_in_group(group)


	def create_group( self, name ):
		""" create new application group
		"""
		groups = self.get_groups( name = name )
		if groups: return groups[0]

		group = self.scheme.create_group( name = name )
		#group.name = name

		return group



	def create_admins_group( self ):
		""" create admin group if not exists
		"""
		admins = self.scheme.create_admins_group()
		if not self.rules( admins, 'a' ):
			self.add_rule( admins, 'a' )
			self.save()




	def get_groups( self, name=None, guid=None, user=None ):
		""" get application groups
		"""
		return self.scheme.get_groups( name=name, guid=guid, user=user )


	def get_admin( self ):
		"""get application admin user
		"""
		return self.scheme.get_admin()

	def list_rules(self, subject=None, access=None):
		return DbACLObject.get_rules(self.scheme, subject,access)
		
	def force_remove_rule( self, subject, access, force=True ):
		""" special remove for application.
		"""
		if not subject: return

		if subject.is_admin() and access == 'a' and not force:
			return

		DbACLObject.force_remove_rule( self, subject, access, force )


	def child_objects(self, guid=None, type=None, name=None, recursive=False):
		""" return list of child objects
		"""
		if not recursive: return super(DbACLApplication, self).child_objects(guid, type, name, recursive)
		

		object_type_list = self.listify(type)
		guid_list = self.listify(guid)
		name_list = self.listify(name)

		condition1 = [ ('guid != ?', self.guid) ] #Not inclued myself
		condition2 = [ ('object_type = ?', item) for item in object_type_list]
		condition3 = {'guid': guid_list}
		condition4 = [ ('name = ?', item) for item in name_list]
	
		raw_result = self.connection.select_cmd('aclobject', _pack_scheme, [condition1, condition2, condition3, condition4])

		result = [DbACLObject(child_tuple, self.scheme, is_new=False) for child_tuple in raw_result]
		result.sort( cmp=lambda a,b: cmp(a.name, b.name) )

		return result