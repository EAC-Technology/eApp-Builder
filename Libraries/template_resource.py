
from utils_base_classes import TemplateCollection
from urls import reverse_api

RESOURCE_OBJECT_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2>{name}</h2>
	  <p>{name}</p>
	  <p>
		<div class="btn-group" role="group">
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


RESOURCE_OBJECT_NEW_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2 class="text-muted">Create Resource</h2>
	  <p class="text-muted">Just hit me</p>
	  <p>
		<button type="button" class="btn btn-success" onclick="{open_create_dialog};">Create</button>
	  </p>
	</div>

""".format(open_create_dialog=reverse_api('app_res:create_form_show', fade=0))


class ResourceListTemplate(TemplateCollection):
	template = RESOURCE_OBJECT_HTML
	new_object_template = RESOURCE_OBJECT_NEW_HTML
	serializable = True
	escape_list = ['name']

	def context(self, app_res):
		return dict(
			name=app_res.name,
			open_update_dialog=reverse_api(
				'app_res:update_form_show', res_id=app_res.guid, command='update'),
			open_delete_dialog=reverse_api(
				'app_res:update_form_show', res_id=app_res.guid, command='delete'),
		)

