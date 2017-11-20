import ProAdmin

# define serialization format
import json

# define serializationt
Serialization = json



# def debug_print( *args ):
# 	marker = args[-1]
# 	if len( str(marker) ) == 1:
# 		args = args[ :-1 ]
# 	else:
# 		marker = '-'
# 	marker = marker or '-'

# 	text = [ '%s' % s for s in args ]
# 	text = ', '.join( text )

# 	debug( '' )
# 	debug( marker * 35 )

# 	debug( '%s' % text )

# 	debug( marker * 35 )
# 	debug( '' )




class APIFormat( object ):
	""" implement methods for create reponses of Remote API methods
	"""
	@classmethod
	def success_result( self, args=None ):
		return Serialization.dumps( [ 'success', args ] )

	@classmethod
	def error_result( self, args=None ):
		return Serialization.dumps( [ 'error', args ] )

	@classmethod
	def request( self, app_guid, data ):
		return Serialization.dumps( [ app_guid, data ] )

	@classmethod
	def parse_response( self, response ):
		try:
			response = Serialization.loads( response )
		except:
			response = response.rsplit( '\n', 1 )[0] # remove sid-code (VDOMService bug)
			response = Serialization.loads( response )

		status = response[0] if len( response ) > 0 else None
		result = response[1] if len( response ) > 1 else None

		return (status, result)







# ------------------------------------------------------------------------------------------------------------------------------------------------------------
#		FORMAT CLASSES
# ------------------------------------------------------------------------------------------------------------------------------------------------------------


class SyncFormat( object ):
	""" Base class for all formats
	"""
	def __init__( self ):
		self.structure 	= [
			'SyncObject', 	# type
			{} 				# attributes
		]

	@property
	def type( self ):
		return self.structure[ 0 ]

	@type.setter
	def type( self, value ):
		self.structure[ 0 ] = value

	@property
	def attributes( self ):
		return self.structure[ 1 ]

	@attributes.setter
	def attributes( self, value ):
		self.structure[ 1 ] = value


	def get_object( self ):
		return self._deserialize()


	def _serialize( self, object ):
		pass

	def _deserialize( self ):
		pass

	@classmethod
	def from_object( self, object ):
		return self()._serialize( object )

	@classmethod
	def from_structure( self, structure ):
		result = self()
		result.structure = structure

		return result



class ACLObjectSyncFormat( SyncFormat ):
	""" Format for ACLObject-instances
	"""
	def __init__( self ):
		SyncFormat.__init__( self )
		self.type = 'ACLObject'


	def _serialize( self, object ):
		if not object:
			return None

		# get object rules
		rules = {}
		for rule in object.rules():
			if not rule.subject:
				rule.delete()
				continue

			subject_guid = rule.subject.guid

			if subject_guid not in rules:
				rules[ subject_guid ] = []

			rules[ subject_guid ].append( rule.access )

		self.attributes =  {
			'guid'		: object.guid,
			'name'		: object.name,
			'type'		: object.type,
			'rules'		: rules,
			'parent'	: object.parent.guid if object.parent else None,
			'childs'	: [ child.guid for child in object.child_objects() ],
		}

		return self


	def _deserialize( self ):
		args = self.attributes

		guid = args[ 'guid' ]
		type = args[ 'type' ]
		name = args[ 'name' ]

		parent_guid = args[ 'parent' ]

		# get parent object
		parent = ProAdmin.application() if not parent_guid else ProAdmin.application().get_by_guid( parent_guid )

		if not parent:
			return None

		object = parent.get_by_guid( guid )
		if not object:
			object = parent.create_child( name=name, type=type )

		object.guid = guid
		object.name = name

		
		rules = args[ 'rules' ]
		
		# get needed application subjects
		app = ProAdmin.application()
		subjects = [ app.get_subject(g) for g in rules ]
		subjects = { s.guid : s for s in subjects if s }

		# remove old rules
		for rule in object.rules():
			if rule.access not in rules.get( rule.subject.guid, [] ):
				object.remove_rule( rule.subject, rule.access )
		
		# set new rules
		for subject_guid in rules:
			subject = subjects.get( subject_guid, None )
			[ object.add_rule( subject, right ) for right in rules[ subject_guid ] if subject and right ]

		return object




class UserSyncFormat( SyncFormat ):
	""" Format for User-instances
	"""
	def __init__( self ):
		SyncFormat.__init__( self )
		self.type = 'User'


	def _serialize( self, user ):
		if not user:
			return None

		self.attributes = {
			'guid'					: user.guid,
			'email'					: user.email,
			'first_name'			: user.first_name,
			'last_name'				: user.last_name,
			'phone'					: user.phone,
			'password'				: user.password,
			'notification_email'	: user.notification_email,
			'cell_phone'			: user.cell_phone,
			'country'				: user.country,
			'keywords'				: user.keywords,
			'root'					: True if ProAdmin.scheme().get_option( 'root_user' ) == user.email else False,
		}

		return self


	def _deserialize( self ):
		args = self.attributes

		guid 	= args[ 'guid' ]
		email 	= args[ 'email' ]

		# check if user exist
		user = ProAdmin.application().create_user( email=email )

		user.guid 		= guid
		user.first_name = args[ 'first_name' ]
		user.last_name 	= args[ 'last_name' ]
		user.phone 		= args[ 'phone' ]
		user.cell_phone = args[ 'cell_phone' ]
		user.country 	= args[ 'country' ]
		user.keywords	= args[ 'keywords' ]
		user.notification_email = args[ 'notification_email' ]
		user.set_password_hash( args[ 'password' ] )

		if args.get( 'root', False ):
			ProAdmin.scheme().set_option( 'root_user', user.email )

		return user





class GroupSyncFormat( SyncFormat ):
	""" Format for Group-instances
	"""
	def __init__( self ):
		SyncFormat.__init__( self )
		self.type = 'Group'

	def _serialize( self, group ):
		if not group:
			return None

		# get group's users guids
		members = [ user.guid for user in group.get_users() ]

		self.attributes = {
			'guid'		: group.guid,
			'name'		: group.name,
			'members'	: members,
		}

		return self



	def _deserialize( self ):
		args = self.attributes

		guid 	= args[ 'guid' ]
		name 	= args[ 'name' ]
		members = args[ 'members' ]

		# check if group exist
		#groups = ProAdmin.application().get_groups( guid=guid )

		# skip Everyone group
		#if groups and groups[0]._is_everyone_group():
		#	return groups[0]

		group = ProAdmin.application().create_group( name=name )
		group.guid = guid
		
		group.user_guid_list = members

		# delete all users from group
		#[ group.remove_user( user ) for user in group.get_users() ]

		# add new list
		#for user_guid in members:
		#	users = ProAdmin.application().get_users( guid=user_guid )
		#	[ group.add_user( users[0] ) if users else None ]

		return group




class SubjectSyncFormat( SyncFormat ):
	""" Common subjects-format
	"""
	@classmethod
	def from_object( self, subject ):
		if subject.is_user():
			return UserSyncFormat.from_object( subject )

		if subject.is_group():
			return GroupSyncFormat.from_object( subject )

		return None


	@classmethod
	def from_structure( self, subject_struct ):
		if subject_struct[0].lower() == 'user':
			return UserSyncFormat.from_structure( subject_struct )

		if subject_struct[0].lower() == 'group':
			return GroupSyncFormat.from_structure( subject_struct )

		return None






# ------------------------------------------------------------------------------------------------------------------------------------------------------------
#		SYNC CLASS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------



class RemoteSync( object ):

	API_OBJECTS_PER_REQUEST = 100 # limitation of structures for one api call request


	# --------------------
	#	SUBJECTS
	# --------------------

	@classmethod
	def _create_subject_structures( self, subjects ):
		return [ SubjectSyncFormat.from_object( subj ).structure for subj in subjects ]


	@classmethod
	def get_subjects_structures( self ):
		return self._create_subject_structures( ProAdmin.application().get_subjects() )


	@classmethod
	def apply_subjects_structures( self, structures ):
		# accept new users
		subject_formats = [ SubjectSyncFormat.from_structure( structure ) for structure in structures ]
		self.apply_users_formats(subject_formats)
		self.apply_groups_formats(subject_formats)

	@classmethod
	def apply_users_formats(self, subject_formats):
		user_formats = [f for f in subject_formats if f.type=="User"]

		remote_users = [ format.get_object() for format in user_formats ]
		existing_users = ProAdmin.application().get_users()

		# remove old application subjects
		dirty = False
		remote_guids = [ subject.guid for subject in remote_users ]
		for existing_user in existing_users:
			if existing_user.guid not in remote_guids:
				existing_user.delete()
				dirty = True
				#print "OLD"

		#add new one
		if dirty: existing_users = ProAdmin.application().get_users()
		dirty = False
		existing_guids = [u.guid for u in existing_users]
		for remote_user in remote_users:
			if remote_user.guid not in existing_guids:
				remote_user.save()
				dirty = True
				#print "NEW"

		#change 
		if dirty: existing_users = ProAdmin.application().get_users()
		for existing_user in existing_users:
			remote_user = [u for u in remote_users if u.guid == existing_user.guid][0]
			if not existing_user == remote_user:
				remote_user.save()
				#print "CHANGE"


	@classmethod
	def apply_groups_formats(self, subject_formats):
		group_formats = [f for f in subject_formats if f.type=="Group"]

		remote_groups = [ format.get_object() for format in group_formats ]
		existing_groups = ProAdmin.application().get_groups()

		# remove old application subjects
		dirty = False
		remote_guids = [ subject.guid for subject in remote_groups ]
		for existing_group in existing_groups:
			if existing_group.guid not in remote_guids:
				existing_group.delete()
				dirty = True
				#print "OLD G"

		#add new one
		if dirty: existing_groups = ProAdmin.application().get_groups()
		dirty = False
		existing_guids = [u.guid for u in existing_groups]
		for remote_group in remote_groups:
			if remote_group.guid not in existing_guids:
				remote_group.save()
				dirty = True
				#print "NEW G"

		#change 
		if dirty: existing_groups = ProAdmin.application().get_groups()
		for existing_group in existing_groups:
			existing_group.get_users()
			remote_group = [u for u in remote_groups if u.guid == existing_group.guid][0]
			if not (existing_group == remote_group and set(existing_group.user_guid_list) == set(remote_group.user_guid_list)):
				if existing_group._is_everyone_group():
				    continue
				remote_group.save()
				#print "CHANGE G"



	# --------------------
	#	OBJECTS
	# --------------------

	@classmethod
	def sort_aclobjects( self, objects ):
		""" sort list of acl objects by tree-level. Firstly root than first level, second etc
		"""
		objects = objects or []

		def compare( a,b ):
			# ??
			i = len( a.guid )
			j = len( a.guid )
			return cmp( i, j )

		objects.sort( cmp=compare )
		return objects


	@classmethod
	def get_dirty_objects( self, root=None, limit=None ):
		""" return list of objects that need to sync
		"""
		if not root:
			ProAdmin.application().refresh()
			root = ProAdmin.application()
			
		return [ root ] if root.is_dirty() else []
		
		objects = []
		def deep( obj ):
			if limit is not None and len( objects ) >= limit:
				return

			if obj.is_dirty():
				objects.append( obj )
			
			# sync of objects disabled
			#for o in obj.child_objects():
			#	deep( o )

		deep( root )
		
		return self.sort_aclobjects( objects )


	@classmethod
	def _create_object_structures( self, objects ):
		return [ ACLObjectSyncFormat.from_object( obj ).structure for obj in objects ]


	@classmethod
	def get_objects_structures( self, root=None ):
		"""
		"""
		if not root:
			root = ProAdmin.application()

		objects = self.get_dirty_objects( root )
		return self._create_object_structures( objects )



	@classmethod
	def apply_objects_structures( self, structures, rights_only=False ):
		""" apply changes from update (commit) arguments
		"""
		# disable deleting of child objects if rights_only mode
		delete_childs = False if rights_only else True

		def is_equal( a,b ):
			""" compare acl objects
			"""
			return False # TODO: compare by rules

			if not a or not b: return False
			
			# compare guids
			if a.guid != b.guid: return False

			# compare names:
			if a.name != b.name: return False

			# compare type
			if a.type != b.type: return False

			return True




		def deep_update( object_guid ):
			""" update chain from object to parent to parent to.. root-object
				remove updated object from dictionary
			"""
			object_struct = objects.pop( object_guid )

			# get parent guid
			parent_guid = object_struct[1][ 'parent' ]

			# check may be parent in upadte-dictionary
			if parent_guid and parent_guid in objects:
				deep_update( parent_guid )

			object_format = ACLObjectSyncFormat.from_structure( object_struct )
			object = object_format.get_object()
			if not object: return 

			# get old ACL object
			old_obj = ProAdmin.application().get_by_guid( object.guid )

			# restore object attributes if rights_only mode
			if rights_only:
				if not old_obj: return
				object.name = old_obj.name
				# TODO: maybe another attributes

			#ignore childs due to disable objets sync
			# remove childs if need
			#childs = object_format.attributes.get( 'childs', None )
			#childs = childs if childs is not None else [ child.guid for child in object.child_objects() ]

			# delete rules of childs if it's was removed
			#for child in object.child_objects():
			#	if child.guid in childs: continue
			#
			#	if delete_childs:
			#		child.delete( False )
			#	else:
			#		[ r.delete() for r in child.rules() ]


			# compare old object and new object
			# apply new object if it changed

			# if was dirty - need to clear dirty bit
			if not is_equal( object, old_obj ) or old_obj.is_dirty():
				object.is_new = None #not sure if new
				object.clear_dirty_bit()
				object.save()



		objects = { obj[1]['guid']: obj for obj in structures }

		# update it localy
		while( objects ):
			object_guid = objects.keys()[0]
			deep_update( object_guid )












class RemoteSyncClient( RemoteSync ):
	""" implement sync-operations
	"""
	def __init__( self, service ):
		RemoteSync.__init__( self )

		self._service = service
		self._connection = None


	def get_connection( self ):
		if not self._service: return None

		if not self._connection:
			from proadmin_api_connection import APIConnection

			# sync API container
			sync_api = '19a67ddc-a792-41fd-bbee-b5190126b6dc'

			# create connection
			self._connection = APIConnection( self._service, sync_api )
			self._connection.set_application_id( application.id )

		return self._connection


	@property
	def last_error( self ):
		conn = self.get_connection()
		if not conn: return None

		return conn.last_error



	def safe_call( self, action, params=None ):
		from proadmin_api_connection import APIError
		#import pprint
		#print ">>>>safe_call", action
		#pprint.pprint( params );
		#print

		connection = self.get_connection()

		try:
			r = connection.call( action, params )
			#pprint.pprint( r );
			#print
			return r
			
		except APIError as error:
			#print "!!!!", error.message
			self.process_error( error.message )
			


	def process_error( self, error ):
		""" process synchronization API errors
		"""
		if error == 'ApplicationIsNotRegistered':
			# Application was deleted in ProAdmin - now need to switch scheme to local
			
			# remove remote settings
			from proadmin_remote_settings import RemoteSettings
			RemoteSettings.delete()

			# unregister current scheme
			ProAdmin.stop_sync()
			ProAdmin.unregister_default_scheme()



	def register( self ):
		""" register Application in ProAdmin
		"""
		# create application
		connection = self.get_connection()
		scheme = ProAdmin.application().scheme

		connection.set_application_id( scheme.guid )

		# create ACLObjectTypes structures
		objecttypes = []
		for obj_type in scheme.get_aclobjecttypes():
			structure = {
				'guid'  			: obj_type.guid,
				'name'  			: obj_type.name,
				'icon'  			: obj_type.icon.get_resource_url() if obj_type.icon else '',
				'access_rights'  	: obj_type.get_access_types(),
			}

			objecttypes.append( structure )

		# prepare call arguments
		args = {
			'object_guid'		: scheme.guid,
			'name'				: scheme.name,
			'icon'				: scheme.get_application_icon_url() if scheme.icon else '',
			'acl_objecttypes'	: objecttypes,
			'api_guid'			: scheme.get_option( 'api_guid', '' ),
			'hosts'				: ProAdmin.hosts(),
		}

		return connection.call( 'register', args )


	def register_sync( self ):
		# update objects
		self.update_objects( rights_only=True, register_sync=True )

		# commit all objects
		self._commit_all_objects()




	def get_registered_applications( self ):
		result = self.safe_call( 'registred_applications' )
		return result

	def get_registred_applications( self, *args, **kwargs ):
		""" obsolete. need for compatibility
		"""
		return self.get_registered_applications( *args, **kwargs )



	def update_subjects( self ):
		# as ksubjects from proadmin
		structs = self.safe_call( 'update_subjects' ) or []
		if not structs: return

		# apply structures
		self.apply_subjects_structures( structs )



	def update_objects( self, rights_only=False, register_sync=False ):		
		limit 	= RemoteSync.API_OBJECTS_PER_REQUEST
		args 	= {}
		objects = []

		# call list of objects for register sync
		if register_sync:
			args = {
				'register_sync_update'	: True,
			}

			objects = self.safe_call( 'update_objects', args )


		while True:
			# call concrete list of objects for register sync
			if register_sync:
				args = {
					'register_sync_update'	: True,
					'objects'				: objects[ :limit ],
				}

				objects = objects[ limit: ]

			# ask objects from ProAdmin application
			structs = self.safe_call( 'update_objects', args ) or []
			if self.last_error is not None: return
			if not structs: return

			# apply it locally
			self.apply_objects_structures( structs, rights_only )



	def commit_objects( self, objects=None ):
		limit = RemoteSync.API_OBJECTS_PER_REQUEST
		if objects: objects = self.sort_aclobjects( objects )

		# implement commit method by parts of data
		while True:
			# get part of data from obejcts list or from application dirty objects
			part = []
			if objects is None:
				part = self.get_dirty_objects( limit=limit )
			else:
				part = objects[ :limit ]
				objects = objects[ limit: ]

			if not part: return

			structs = self._create_object_structures( part )
			self.safe_call( 'commit_objects', structs )
			if self.last_error is not None: return

			# clear dirty-bit
			for obj in part:
				obj.clear_dirty_bit()
				obj.save()



	def _commit_all_objects( self ):
		objects = [ ProAdmin.application() ] #+ ProAdmin.application().child_objects( recursive=True ) #disable object sync except for application
		return self.commit_objects( objects )



	def check_password( self, email, password ):
		result = self.safe_call( action_name = 'check_password', params = { 'login': email, 'password': password } )
		return result



	def proadmin_version( self, details=False ):
		try:
			params = { 'details' : details }
			return self.safe_call( 'version', params )
		except:
			pass

		if self.get_registred_applications():
			return 'less than v.1.1.06'

		return None


	def create_user( self ):
		pass


	def create_group( self, name, users=None ):
		if not name: return None
		users = users or []

		params = {
			'name'		: name,
			'users'		: users,
		}

		return self.safe_call( 'create_group', params )















class RemoteSyncServer( RemoteSync ):

	def __init__( self ):
		RemoteSync.__init__( self )

		self.guid_map = {}



	def guid( self, guid ):
		""" guid-mapping
		"""
		if guid in self.guid_map:
			return self.guid_map[ guid ]

		return guid



	def commit_objects( self, real_guid, app, args ):
		""" implementation of commit objects in server
		"""
		# update guids by map
		self.guid_map[ real_guid ] = app.guid

		for obj in args:
			obj[1]['guid'] 		= self.guid( obj[1]['guid'] )
			obj[1]['parent']	= self.guid( obj[1]['parent'] )

		RemoteSync.apply_objects_structures( args )




	def update_objects( self, real_guid, app, args ):
		"""
		"""
		args 	= args or {}
		limit 	= RemoteSync.API_OBJECTS_PER_REQUEST
		objects = []

		# for first sync get objects from session
		if 'register_sync_update' in args:
			
			# return list of all guids for first request
			if 'objects' not in args:
				childs = app.child_objects( recursive=True )
				return [ o.guid for o in self.sort_aclobjects( childs )  ]
			
			# get objects for asked guids
			guids = args.get( 'objects', [] )
			objects = [ app.get_by_guid( g ) for g in guids ]
		
		else:
			objects = self.get_dirty_objects( root=app, limit=limit )
		
		structs = self._create_object_structures( objects )

		# modify guids
		self.guid_map[ app.guid ] = real_guid
		self.guid_map[ ProAdmin.application().guid ] = ''

		for s in structs:
			s[1]['guid'] 	= self.guid( s[1]['guid'] )
			s[1]['parent'] 	= self.guid( s[1]['parent'] )

		# clear dirty objects
		for obj in objects:
			obj.clear_dirty_bit()
			obj.save()

		return structs



	def update_subjects( self, app, args ):
		"""
		"""
		return RemoteSync.get_subjects_structures()


	def check_password( self, app, args ):
		email = args[ 'login' ]
		password = args[ 'password' ]

		users = ProAdmin.application().get_users( email )
		user = users[0] if users else None

		if not user: return False
		return user.check_password( password )



	def create_group( self, app, args ):
		""" create group in ProAdmin from SYNC API
		"""
		return ProAdmin.create_group( name=args.get('name'), users=args.get('users') )


	def create_user( self, app, args ):
		"""
		"""
		pass

