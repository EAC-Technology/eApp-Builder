class Rule( object ):
	""" class for represent ACL Rule
	"""
	def __init__( self, object=None, subject=None, access=None):
		self.object 	= object
		self.subject 	= subject
		self.access 	= access


	def delete( self ):
		""" delete rule with admins protection
		"""
		return self.force_delete( force=False )


	def force_delete( self, force=True ):
		""" delete rule for admins too
		"""
		if self.object and self.subject:
			self.object.force_remove_rule( self.subject, self.access, force )
			self.object.save()



	def __eq__( self, other ):
		if not other: return False
		return self.object.guid == other.object.guid and self.subject.guid == other.subject.guid and self.access == other.access



	def __hash__( self ):
		return hash( self.object.guid + self.subject.guid + self.access )



	def __str__( self ):
		obj_name 	= self.object.guid
		subj_name 	= self.subject.guid
		access_text = self.access if self.access else ''

		return "Rule: (" + obj_name + ', ' + subj_name + ", '" + access_text + "')"

	def __repr__(self):
		return self.__str__()


	# -------------------------------------------------------------------
	# 		Retreive methods
	# -------------------------------------------------------------------

	@classmethod
	def get_rules( self, object, subject=None, access=None ):
		""" retreive rules for object
		"""
		if not object:
			return []

		if not subject: subject = []
		if not access:	access 	= []

		# make lists from arguments
		if not isinstance( subject, list ):
			subject = [ subject ]

		if not isinstance( access, list ):
			access	= [ access ]

		# get subject guids list
		guids = []
		for s in subject:
			guids += s.get_guid_list()
		guids = list( set(guids) )

		app 		= object.scheme.application
		tuples 		= object.get_rules_tuples()

		# create result rules
		result = []

		for guid, rule in tuples:
			if ( guid in guids or not guids ) and ( rule in access or not access ):
				subject = app.get_subject( guid = guid )
				if subject:
					result.append( Rule( object, subject, rule ) )

		return result



	@classmethod
	def fast_rules( self, object=None, subject=None, access=None, recursive=False, get_empty=False ):
		""" fast implementation for rules retreive. return rule like tuple of guids: (obj, subj, access)
		"""
		import ProAdmin

		if not object: object = ProAdmin.application()
		if not subject: subject = []
		if not access:	access 	= []

		# make lists from arguments
		if not isinstance( subject, list ):
			subject = [ subject ]

		if not isinstance( access, list ):
			access	= [ access ]

		# get subject guids list
		subjects = []
		for s in subject:
			subjects += s.get_guid_list()
		subjects = list( set(subjects) )


		result = []

		# check root object
		rules_tuples = object.get_rules_tuples()
		for subj, right in rules_tuples:
			if ( subj in subjects or not subjects ) and ( right in access or not access ):
				rule = ( object.guid, subj, right )
				result.append( rule )

		if get_empty and not rules_tuples:
			rule = ( object.guid, None, None )
			result.append( rule )

		if not recursive:
			return result


		# fix for dubling
		result = []


		# filter for get only objects
		filter = '(|(objectClass=document)(objectClass=organizationalUnit))'

		# generate subjects-access filter
		subj_filter = ''

		for guid in subjects:
			if not access:
				subj_filter += '(description=%s,%s)' % (guid, '*')
				continue

			for a in access:
				subj_filter += '(description=%s,%s)' % (guid, a)

		if subj_filter:
			filter += '(|%s)' % subj_filter
			filter = '(&%s)' % filter


		# execute query
		connection = object.scheme.connection
		objects = connection.search( object.ldapobject.dn, filter, recursive=recursive )

		for o in objects:
			o_guid = o.attributes.get('documentIdentifier', [''])[0]

			# if no rules for this ACL object but need all
			if get_empty and o.attributes.get('description', None) is None:
				rule = ( o_guid, None, None )
				result.append( rule )
				continue

			# process rules for this ACL object
			for description in o.attributes.get('description', []):
				if ',' not in description:
					description += ','

				s_guid, a_letter = description.split( ',' )
				if subjects and s_guid not in subjects: continue
				if access and a_letter not in access: continue

				rule = ( o_guid, s_guid, a_letter )
				result.append( rule )

		return result

