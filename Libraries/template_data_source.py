
from utils_base_classes import TemplateCollection
from urls import reverse_api


DATA_SOURCE_OBJECT_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2>{connector}</h2>
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


DATA_SOURCE_OBJECT_NEW_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2 class="text-muted">Create Data Source</h2>
	  <p class="text-muted">Just hit me</p>
	  <p>
		<button type="button" class="btn btn-success" onclick="{open_create_dialog};">Create</button>
	  </p>
	</div>

""".format(open_create_dialog=reverse_api('data_source:create_form_show', fade=0))


class DataSourceTemplateCollection(TemplateCollection):
	template = DATA_SOURCE_OBJECT_HTML
	new_object_template = DATA_SOURCE_OBJECT_NEW_HTML
	serializable = True
	escape_list = ['name', 'connector']

	def context(self, data_source):
		return dict(
			name=data_source.name,
			connector=data_source.connector,
			open_update_dialog=reverse_api(
				'data_source:update_form_show', data_source_id=data_source.guid, command='update'),
			open_delete_dialog=reverse_api(
				'data_source:update_form_show', data_source_id=data_source.guid, command='delete'),
		)

