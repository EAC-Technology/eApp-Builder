try:
	import localization
	from widget_localization import LocalizationWidget

	from models import Workspace
	from urls import reverse
	from templates import ApplicationTemplateCollection, WidgetTemplateCollection, DataSourceTemplateCollection

	lang = localization.get_lang()

	if not 'id' in request.arguments:
		response.redirect(reverse('main'))

	workspace_id = request.arguments.get('id')
	workspace = Workspace.get(guid=workspace_id)

	if not workspace:
		response.redirect(reverse('main'))

	apps = workspace.applications
	widgets = workspace.widgets
	data_sources = workspace.data_sources

	self.hpt_main.htmlcode += ApplicationTemplateCollection(apps, many=True, add_new=True).html
	self.hpt_main.htmlcode += WidgetTemplateCollection(widgets, many=True, add_new=True).html
	self.hpt_main.htmlcode += DataSourceTemplateCollection(data_sources, many=True, add_new=True).html

	# fill workspace_id in all edit forms of current pager
	self.cnt_widget.dialog_create.form_create.workspace_id.value = workspace.guid
	self.cnt_widget.dialog_update.form_update.workspace_id.value = workspace.guid
	self.cnt_data_source.dialog_create.form_create.workspace_id.value = workspace.guid
	self.cnt_data_source.dialog_update.form_update.workspace_id.value = workspace.guid
	self.cnt_application.dialog_create.form_create.workspace_id.value = workspace.guid
	self.cnt_application.dialog_update.form_update.workspace_id.value = workspace.guid

except Exception, ex:
	from app_settings import settings
	from vdom_debug import p_ex

	if settings.TEST_MODE:
		p_ex()

	self.growl.title = lang['error']
	self.growl.text = lang['unknown_error']
	self.growl.active = "1"
