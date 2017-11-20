from models import Workspace
from templates import WorkspaceTemplateCollection

command = request.arguments.get('command', '')

if command == 'delete':

	if not 'workspace_id' in request.arguments:
		raise Exception('Workspace ID is not provided')

	workspace_id = request.arguments['workspace_id']
	workspace = Workspace.get(guid=workspace_id)

	if workspace:
		workspace.delete()
		self.dialog_update.show = '0'

elif command == 'create':
	title = request.arguments['title']
	description = request.arguments['description']
	if title:
		new_workspace = Workspace(name=title, description=description)
		new_workspace.save()

elif command == 'update':
	workspace_id = request.arguments['workspace_id']
	title = request.arguments['title']
	description = request.arguments['description']

	workspace = Workspace.get(guid=workspace_id)

	if workspace and title:
		workspace.name = title
		workspace.description = description
		workspace.save()

		self.dialog_update.show = '0'

self.hpt_main.htmlcode = u'{}'.format(
	WorkspaceTemplateCollection(Workspace.all(), many=True, add_new=True).html
)
