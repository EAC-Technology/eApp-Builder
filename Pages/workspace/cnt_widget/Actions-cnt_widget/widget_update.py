from models import Workspace, Widget
from templates import WorkspaceTemplateCollection, BreadcrumbTemplate
from urls import reverse

if 'workspace_id' not in request.arguments:
	raise Exception('Workspace ID is not provided')

workspace_id = request.arguments.get('workspace_id')
command = request.arguments.get('command', u'')

workspace = Workspace.get(guid=workspace_id)

if not workspace:
	self.action('goTo', ['/main'])

elif command in ['delete', 'update']:

	if 'widget_id' not in request.arguments:
		raise Exception(u'Widget ID is not provided')
	widget_id = request.arguments['widget_id']
	widget = Widget.get(guid=widget_id, workspace_id=workspace.guid)

	if widget:
		if command == 'delete':
			widget.delete()
		else:
			title = request.arguments['title']
			if title:
				widget.name = title
				widget.save()

	self.dialog_update.action('hide', ['0'])

elif command == 'create':
	title = request.arguments['title']
	if title:
		widget = Widget()
		widget.workspace_id = workspace.guid
		widget.name = title
		widget.save()
