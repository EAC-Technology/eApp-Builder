from models import Application, Workspace, Resource, AppScript
from templates import (ViewTemplateCollection, RoleTemplateCollection,
	RightTemplateCollection, ResourceListTemplate, ScriptTemplateCollection)
from urls import reverse


application_id = request.arguments.get('application_id')
app = Application.get(guid=application_id) if application_id else None
if app:
	self.tab_app.tab_view.hpt_views.htmlcode = ViewTemplateCollection(app.views, many=True, add_new=True).html
	self.tab_app.tab_resources.hpt_resources.htmlcode = ResourceListTemplate(app.resources, add_new=True).html
	self.tab_app.tab_script.hpt_scripts.htmlcode = ScriptTemplateCollection(app.scripts, add_new=True).html

workspace_id = request.arguments.get('workspace_id')
workspace = Workspace.get(guid=workspace_id) if workspace_id else None
if workspace:
	self.tab_app.tab_roles.hpt_roles.htmlcode = RoleTemplateCollection(workspace.roles, many=True, add_new=True).html
	self.tab_app.tab_roles.hpt_roles.htmlcode += RightTemplateCollection(workspace.rights, many=True, add_new=True).html
