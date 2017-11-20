
from utils_base_classes import TemplateCollection
from urls import reverse_api

VIEW_OBJECT_HTML = u"""

	<div class="eapp_object eapp_object_view col-xs-6 col-lg-4">
	  <h2>{name}</h2>
	  <p>{name}</p>
	  <p>
		<div class="btn-group" role="group">
			<button type="button" class="btn btn-info" onclick="{play_view_test};">
				<span class="glyphicon glyphicon-play" aria-hidden="true"></span>
			</button>
			<button type="button" class="btn btn-default" onclick="{open_update_dialog};">
				<span class="glyphicon glyphicon-cog" aria-hidden="true"></span>
			</button>
		</div>
		<button type="button" class="btn pull-right" onclick="{open_delete_dialog};">
			<span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
		</button>
	  </p>
	</div>

"""


VIEW_OBJECT_NEW_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2 class="text-muted">Create View</h2>
	  <p class="text-muted">Just hit me</p>
	  <p>
		<button type="button" class="btn btn-success" onclick="{open_create_dialog};">Create</button>
	  </p>
	</div>

""".format(open_create_dialog=reverse_api('app_view:create_form_show', fade=0))


class ViewTemplateCollection(TemplateCollection):
	template = VIEW_OBJECT_HTML
	new_object_template = VIEW_OBJECT_NEW_HTML
	serializable = True
	escape_list = ['name']

	def context(self, app_view):
		return dict(
			name=app_view.name,
			open_update_dialog=reverse_api(
				'app_view:update_form_show', view_id=app_view.guid, command='update'),
			play_view_test=reverse_api(
				'app_view:update_form_show', view_id=app_view.guid, command='play'),
			open_delete_dialog=reverse_api(
				'app_view:update_form_show', view_id=app_view.guid, command='delete'),
		)

