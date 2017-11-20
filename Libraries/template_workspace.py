
from urls import reverse, reverse_api
from utils_base_classes import TemplateCollection


WORKSPACE_OBJECT_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2>{name}</h2>
	  <p>{description}</p>
	  <p>
		<div class="btn-group" role="group">
			<a class="btn btn-default" href="{link}" role="button">Open &raquo;</a>
			<button type="button" class="btn btn-default" onclick="{open_update_dialog};">
				<span class="glyphicon glyphicon-cog" aria-hidden="true"></span>
			</button>
			<button type="button" class="btn btn-warning" onclick="{open_delete_dialog};">
				<span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
			</button>
		</div>
	  </p>
	</div>

"""

WORKSPACE_OBJECT_NEW_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2 class="text-muted">Create Workspace</h2>
	  <p class="text-muted">Just hit me</p>
	  <p>
		<button type="button" class="btn btn-success" onclick="{open_create_dialog};">Create</button>
	  </p>
	</div>

""".format(open_create_dialog=reverse_api('workspace:create_form_show', fade=0))


class WorkspaceTemplateCollection(TemplateCollection):
	template = WORKSPACE_OBJECT_HTML
	new_object_template = WORKSPACE_OBJECT_NEW_HTML
	serializable = True
	escape_list = ['name', 'description']

	def context(self, workspace):
		return dict(
			id=workspace.guid,
			name=workspace.name,
			description=workspace.description,
			link=reverse('workspace', workspace_id=workspace.guid),
			open_update_dialog=reverse_api('workspace:update_form_show', workspace_id=workspace.guid, command='update'),
			open_delete_dialog=reverse_api('workspace:update_form_show', workspace_id=workspace.guid, command='delete'),
		)
