try:
	import localization
	from models import Workspace
	from templates import WorkspaceTemplateCollection
	from urls import reverse
	from widget_localization import LocalizationWidget
	import json

	lang = localization.get_lang()

	workspaces = Workspace.all()

	if not workspaces:
		self.hpt_main.htmlcode += '<h2>No workspaces in the system</h2>'
	else:
		template_workspace = WorkspaceTemplateCollection(workspaces, add_new=True)
		self.hpt_main.htmlcode += template_workspace.html
		self.obj_workpaces.data = template_workspace.json


except Exception, ex:
	from app_settings import settings
	from vdom_debug import p_ex

	if settings.TEST_MODE:
		p_ex()

	self.growl.title = lang['error']
	self.growl.text = lang['unknown_error']
	self.growl.active = "1"
