
from utils_base_classes import TemplateCollection
from urls import reverse_api


VIEW_OBJECT_HTML = u"""
	<a href="#" id="view_item" onclick="{open_acls}" class="list-group-item {is_active}"
		data-toggle="tooltip" data-placement="bottom" title="{object_name}">
		{object_name}
	</a>
"""

ROLE_OBJECT_HTML = u"""
	<a href="#" id="view_item_{object_id}" onclick="{open_acls}" class="list-group-item {is_active}">
		{object_name} {rights_attached}
	</a>
"""

RIGHT_OBJECT_HTML = u"""
	<a href="#" id="view_item_{object_id}" onclick="{open_acls}" class="list-group-item {selected} {view_right}">
		{object_name}
	</a>
"""


VIEW_COLLECTION_HTML = u"""
	<h3>Views</h3>
	<div class="list-group">{objects}</div>
"""


ROLE_COLLECTION_HTML = u"""
	<h3>Roles</h3>
	<div class="list-group">{objects}</div>
"""


RIGHT_COLLECTION_HTML = u"""
	<h3>Rights</h3>
	<div class="list-group">{objects}</div>
"""


ACL_OBJECT_HTML = u"""
  <div class="col-md-4">{acl_object}</div>
"""


class ACLViewTemplateCollection(TemplateCollection):
	template = VIEW_OBJECT_HTML
	collection = VIEW_COLLECTION_HTML
	escape_list = ['object_name']

	def context(self, view):
		return dict(
			object_id=view.guid,
			object_name=view.name,
			is_active='active' if view.guid == self.selected_id else '',
			open_acls=reverse_api('app_acl:select_item', object_id=view.guid, type='view'),
		)


class ACLRoleTemplateCollection(TemplateCollection):
	template = ROLE_OBJECT_HTML
	collection = ROLE_COLLECTION_HTML
	escape_list = ['object_name']
	role_rights = {}  # need to be filled outside

	def context(self, role):
		rights_in_role = self.role_rights.get(role.guid, 0)
		return dict(
			object_id=role.guid,
			object_name=role.name,
			rights_attached=u'<span class="badge">{}</span></a>'.format(rights_in_role) if rights_in_role else u'',
			is_active='active' if role.guid == self.selected_id else '',
			open_acls=reverse_api('app_acl:select_item', object_id=role.guid, type='role'),
		)


class ACLRightTemplateCollection(TemplateCollection):
	template = RIGHT_OBJECT_HTML
	collection = RIGHT_COLLECTION_HTML
	escape_list = ['object_name']

	def context(self, right):
		return dict(
			object_id=right.guid,
			object_name=right.name,
			view_right='list-group-item-info' if right.guid in self.view_rights else '',
			selected='active' if right.guid in self.selected_id else '',
			open_acls=reverse_api('app_acl:select_item', object_id=right.guid, type='right'),
		)


class ACLTableCollection(TemplateCollection):
	template = ACL_OBJECT_HTML

	def context(self, acl_template):
		return dict(
			acl_object=acl_template.html
		)

