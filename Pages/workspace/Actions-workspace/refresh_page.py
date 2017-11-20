from models import Workspace
from templates import WidgetTemplateCollection, DataSourceTemplateCollection, ApplicationTemplateCollection
from urls import reverse

if not 'workspace_id' in request.arguments:
	raise Exception('Workspace ID is not provided')

workspace_id = request.arguments.get('workspace_id')
workspace = Workspace.get(guid=workspace_id)

if not workspace:
	self.action('goTo', [reverse('main')])

apps = workspace.applications
widgets = workspace.widgets
data_sources = workspace.data_sources

if not apps+widgets+data_sources:
	self.hpt_main.htmlcode += '<h2>No childs in the workspace</h2>'
else:
	self.hpt_main.htmlcode += ApplicationTemplateCollection(apps, many=True, add_new=True).html
	self.hpt_main.htmlcode += WidgetTemplateCollection(widgets, many=True, add_new=True).html
	self.hpt_main.htmlcode += DataSourceTemplateCollection(data_sources, many=True, add_new=True).html
