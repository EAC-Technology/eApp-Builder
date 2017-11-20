
from utils_base_classes import TemplateCollection
from urls import reverse_api


OBJECT_HTML = u"""
		<div class="input-group">
		  <input type="text" class="form-control" aria-label="..." readonly value="{object_name}{object_description}"/>
		  <div class="input-group-btn">
			<button type="button" class="btn btn-default" onclick="{open_update_dialog};">
				<span class="glyphicon glyphicon-cog" aria-hidden="true"></span>
			</button>
			<button type="button" class="btn btn-warning" onclick="{open_delete_dialog};">
				<span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
			</button>
		  </div>
		</div>

"""


OBJECT_COLLECTION_HTML = u"""
	<div class="list-group">{objects}</div>
"""


ROLE_OBJECT_NEW_HTML = u"""
	<br/>
	<a href="#" class="" onclick="{open_create_dialog};">
		Create new role
	</a>
""".format(open_create_dialog=reverse_api('app_role:create_form_show', fade=0, type='Role'))


RIGHT_OBJECT_NEW_HTML = u"""
	<br/>
	<a href="#" class="" onclick="{open_create_dialog};">
		Create new right
	</a>
""".format(open_create_dialog=reverse_api('app_role:create_form_show', fade=0, type='Right'))


class RoleTemplateCollection(TemplateCollection):
	template = OBJECT_HTML
	collection = OBJECT_COLLECTION_HTML
	new_object_template = ROLE_OBJECT_NEW_HTML

	def context(self, role):
		return dict(
			object_name=role.name,
			object_description=u': %s' % role.description if role.description else u'',
			open_update_dialog=reverse_api(
				'app_role:update_form_show', object_id=role.guid, command='update', type='role'),
			open_delete_dialog=reverse_api(
				'app_role:update_form_show', object_id=role.guid, command='delete', type='role'),
		)


class RightTemplateCollection(TemplateCollection):
	template = OBJECT_HTML
	collection = OBJECT_COLLECTION_HTML
	new_object_template = RIGHT_OBJECT_NEW_HTML

	def context(self, right):
		return dict(
			object_name=right.name,
			object_description=u': %s' % right.description if right.description else u'',
			open_update_dialog=reverse_api(
				'app_role:update_form_show', object_id=right.guid, command='update', type='right'),
			open_delete_dialog=reverse_api(
				'app_role:update_form_show', object_id=right.guid, command='delete', type='right'),
		)
