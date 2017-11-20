
from utils_base_classes import TemplateCollection
from urls import reverse_api

SCRIPT_OBJECT_HTML = u"""

	<div class="eapp_object eapp_object_script col-xs-6 col-lg-4">
	  <h2>{name}</h2>
	  <p>{name}</p>
	  <p>
		<div class="btn-group" role="group">
			<button type="button" class="btn btn-default" onclick="{play_wholexml_test};">
				<span class="glyphicon glyphicon-console" aria-hidden="true"></span>
			</button>
			<button type="button" class="btn btn-info" onclick="{play_script_test};">
				<span class="glyphicon glyphicon-play" aria-hidden="true"></span>
			</button>
			<button type="button" class="btn btn-default" onclick="{open_update_dialog};">
				<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
			</button>
		</div>
		<button type="button" class="btn pull-right" onclick="{open_delete_dialog};">
			<span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
		</button>
	  </p>
	</div>

"""


SCRIPT_OBJECT_NEW_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2 class="text-muted">Create Script</h2>
	  <p class="text-muted">Just hit me</p>
	  <p>
		<button type="button" class="btn btn-success" onclick="{open_create_dialog};">Create</button>
	  </p>
	</div>

""".format(open_create_dialog=reverse_api('app_script:create_form_show', fade=0))


class ScriptTemplateCollection(TemplateCollection):
	template = SCRIPT_OBJECT_HTML
	new_object_template = SCRIPT_OBJECT_NEW_HTML
	serializable = True
	escape_list = ['name']

	def context(self, app_script):
		return dict(
			name=app_script.name,
			open_update_dialog=reverse_api(
				'app_script:update_form_show', script_id=app_script.guid, command='update'),
			play_wholexml_test=reverse_api( 'app_script:update_form_show',
				script_id=app_script.guid,
				command='wholexml',
				email='sibirsky.photo@gmail.com',
				eac_token="32b6ecf9-2420-4f80-866e-3678a312e6e1"),
			play_script_test=reverse_api(
				'app_script:update_form_show', script_id=app_script.guid, command='play'),
			open_delete_dialog=reverse_api(
				'app_script:update_form_show', script_id=app_script.guid, command='delete'),
		)

