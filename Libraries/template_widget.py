from urls import reverse, reverse_api
from utils_base_classes import TemplateCollection


WIDGET_OBJECT_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2>{name}</h2>
	  <p>{source}</p>
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

WIDGET_OBJECT_NEW_HTML = u"""

	<div class="eapp_object col-xs-6 col-lg-4">
	  <h2 class="text-muted">Create Widget</h2>
	  <p class="text-muted">Just hit me</p>
	  <p>
		<button type="button" class="btn btn-success" onclick="{open_create_dialog};">Create</button>
	  </p>
	</div>

""".format(open_create_dialog=reverse_api('widget:create_form_show', fade=0))


class WidgetTemplateCollection(TemplateCollection):
	template = WIDGET_OBJECT_HTML
	new_object_template = WIDGET_OBJECT_NEW_HTML
	escape_list = ['name', 'source']

	def context(self, widget):
		return dict(
			id=widget.guid,
			name=widget.name,
			source=widget.source[:30],
			link=reverse('widget', widget_id=widget.guid),
			open_update_dialog=reverse_api('widget:update_form_show', widget_id=widget.guid, command='update'),
			open_delete_dialog=reverse_api('widget:update_form_show', widget_id=widget.guid, command='delete'),
		)
