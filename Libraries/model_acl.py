"""
	ACL related models
"""

from utils_base_classes import DB_model, cached_property
from model_application import Workspace


class Role(DB_model):
	"""
		Role behaves like Group in ProAdmin, but exists inside individual Workspace
	"""

	db_table = 'eapp_role'  # db_table
	fields_list = ['id', 'guid', 'workspace_id', 'name', 'description']
	guid_key = 'guid'  # will generate uuid automatically when created new row

	@property
	def workspace(self):
		return Workspace.get(guid=self.workspace_id) if self.workspace_id else None


class Right(DB_model):
	"""
		Right behaves like Rule in ProAdmin, but exists inside individual Workspace
	"""

	db_table = 'eapp_right'  # db_table
	fields_list = ['id', 'guid', 'workspace_id', 'name', 'description']
	guid_key = 'guid'  # will generate uuid automatically when created new row

	@property
	def workspace(self):
		return Workspace.get(guid=self.workspace_id) if self.workspace_id else None


class ACL(DB_model):
	"""
		Compose a single rule, where object provide a special right to subject
	"""

	db_table = 'eapp_acl'  # db_table
	fields_list = ['id', 'object_id', 'subject_id', 'right_id']

	def __hash__(self):
		return hash((self.object_id, self.subject_id, self.right_id))

	@property
	def hash(self):
		return hash(self)

	def save(self):
		""" Save if object doesn't exist, otherwise delete """
		existing_acl = ACL.get(object_id=self.object_id, subject_id=self.subject_id, right_id=self.right_id)
		if not existing_acl:
			super(ACL, self).save()
		else:
			existing_acl.delete()


class acl_mixin(object):
	"""
		Inherit this to any model based on DB_model to provide interface to work with ACL system
	"""

	def acl_list(self, subject):
		if isinstance(subject, Role):
			subject = subject.guid
		return ACL.filter(object_id=self.guid, subject_id=subject)

	def acl_add(self, object_id, rule_id):
		if not ACL.get(subject_id=self.guid, object_id=object_id, rule_id=rule_id):
			acl = ACL()
			acl.subject_id = self.guid
			acl.object_id = object_id
			acl.rule_id = rule_id
			acl.save()
