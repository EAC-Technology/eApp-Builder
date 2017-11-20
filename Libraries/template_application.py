
from utils_base_classes import TemplateCollection
from urls import reverse_api, reverse


APPLICATION_OBJECT_HTML = u"""

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


APPLICATION_OBJECT_NEW_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2 class="text-muted">Create Application</h2>
	  <p class="text-muted">Just hit me</p>
	  <p>
		<button type="button" class="btn btn-success" onclick="{open_create_dialog};">Create</button>
		<button type="button" class="btn btn-default" onclick="{open_create_dialog};">Import</button>
	  </p>
	</div>

""".format(open_create_dialog=reverse_api('application:create_form_show', fade=0))


class ApplicationTemplateCollection(TemplateCollection):
	template = APPLICATION_OBJECT_HTML
	new_object_template = APPLICATION_OBJECT_NEW_HTML
	serializable = True
	escape_list = ['name', 'description']

	def context(self, app):
		return dict(
			name=app.name,
			description=app.description or "---",
			link=reverse('application', app_id=app.guid),
			open_update_dialog=reverse_api(
				'application:update_form_show', application_id=app.guid, command='update'),
			open_delete_dialog=reverse_api(
				'application:update_form_show', application_id=app.guid, command='delete'),
		)

