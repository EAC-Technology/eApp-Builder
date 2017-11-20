from VEE_std_lib import v_BaseException, base_object
from VEE_utils import 	CachedProperty, AutoCast, v_PropertyReadOnly,\
						AutoCastCachedProperty, nothing_inst

from vscript import error
from vscript.subtypes import generic
import ProAdmin



class v_ProAdminLoginError( v_BaseException ):
	pass

class v_ProAdminEmptyPasswordError( v_BaseException ):
	pass

class v_ProAdminNoCurrentUser( v_BaseException ):
	pass

EXCEPTIONS = {
	ProAdmin.ProAdminLoginError			: v_ProAdminLoginError,
	ProAdmin.ProAdminEmptyPasswordError	: v_ProAdminEmptyPasswordError,
}



class v_user( base_object ):

	@CachedProperty
	def user( self ):
		return self.object


	@AutoCast
	@v_PropertyReadOnly
	def v_groups( self ):
		return map( v_group, self.user.get_groups() )


	@AutoCastCachedProperty
	@v_PropertyReadOnly
	def v_isuser( self ):
		return True


	@AutoCastCachedProperty
	@v_PropertyReadOnly
	def v_notificationemail( self ):
		return self.user.notification_email


	@AutoCastCachedProperty
	@v_PropertyReadOnly
	def v_firstname( self ):
		return self.user.first_name


	@AutoCastCachedProperty
	@v_PropertyReadOnly
	def v_lastname( self ):
		return self.user.last_name


	@AutoCastCachedProperty
	@v_PropertyReadOnly
	def v_cellphone( self ):
		return self.user.cell_phone


	#obsolete methods names
	v_get_groups = v_groups
	v_is_user = v_isuser
	v_notification_email = v_notificationemail



class v_group( base_object ):

	@CachedProperty
	def group( self ):
		return self.object


	@AutoCast
	@v_PropertyReadOnly
	def v_users( self ):
		return map( v_user,  self.group.get_users() )


	@AutoCastCachedProperty
	@v_PropertyReadOnly
	def v_isuser ( self ):
		return False


	#obsolete methods names
	v_get_users = v_users
	v_is_user = v_isuser



class v_application( base_object ):

	def __init__( self, data ):
		base_object.__init__( self, self )
		self._title = data[0]
		self.data = data[1]

	@AutoCast
	@v_PropertyReadOnly
	def v_title(self):
		return self._title

	@AutoCast
	@v_PropertyReadOnly
	def v_ip(self):
		return self.data.get('ip', '')

	@AutoCast
	@v_PropertyReadOnly
	def v_guid(self):
		return self.data.get('guid', '')

	@AutoCast
	@v_PropertyReadOnly
	def v_hosts(self):
		return self.data.get('hosts', [])

	@AutoCast
	@v_PropertyReadOnly
	def v_name(self):
		return self.data.get('name', '')


class v_proadmin( generic ):

	@classmethod
	@AutoCast
	@v_PropertyReadOnly
	def v_accesstokenforuser( self, user ):
		return ProAdmin.sudo_accesstoken( user.user )


	@classmethod
	@AutoCast
	def v_setcurrentuser( self, user = None ):
		ProAdmin.set_user( user.user )


	@classmethod
	@AutoCast
	@v_PropertyReadOnly
	def v_currentuser( self ):
		user = ProAdmin.current_user()
		return 	v_user( user ) if user else nothing_inst


	@classmethod
	@AutoCast
	def v_login( self, email, password ):
		try:
			ProAdmin.login( email, password )
		except Exception, ex:
			cls = EXCEPTIONS.get( ex.__class__, v_BaseException )
			raise cls( ex.message )


	@classmethod
	@AutoCast
	def v_searchuser( self, email = None, guid = None ):
		return map( v_user,  ProAdmin.application().get_users( email, guid ) )


	@classmethod
	@AutoCast
	def v_searchgroup( self, name = None, guid = None ):
		return map( v_group,  ProAdmin.application().get_groups( name, guid ) )


	@classmethod
	@AutoCast
	def v_isuseringroup( self, user, group ):
		group_guid = group.group.guid
		for g in user.user.get_groups():
			if g.guid == group_guid:
				return True

		return False


	@classmethod
	@AutoCast
	def v_registeredapplications( self ):
		return map( v_application, ProAdmin.get_registred_applications().items() )


	#obsolete methods names
	v_set_user = v_setcurrentuser
	v_current_user = v_currentuser
	v_search_users = v_users = v_searchuser
	v_search_groups = v_groups = v_searchgroup
	v_is_user_in_group = v_user_in_group = v_isuseringroup
	v_registered_applcations = v_applications = v_registeredapplications



def authenticated( func ):
	def wrapper( *args, **kwargs ):
		if not ProAdmin.current_user():
			raise v_ProAdminNoCurrentUser( "No logged in user" )
		return func( *args, **kwargs )
	return wrapper



class v_rule( base_object ):

	@CachedProperty
	def rule( self ):
		return self.object

	@CachedProperty
	@v_PropertyReadOnly
	def v_subject( self ):
		subj = self.rule.subject
		return v_user( subj ) if subj.is_user() else v_group( subj )

	@AutoCastCachedProperty
	@v_PropertyReadOnly
	def v_access( self ):
		return self.rule.access



environment = tuple( (  (cls.__name__.lower(), error( cls ) ) for cls in EXCEPTIONS.itervalues() ) ) + \
(	( "v_proadmin",			v_proadmin	), )
