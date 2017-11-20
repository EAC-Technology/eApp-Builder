
from models import Workspace
from templates import TemplateWorkspaceCollection

if not 'workspace_id' in request.arguments:
	raise Exception('Workspace ID is not provided')

workspace_id = request.arguments['workspace_id']
command = request.arguments['command']

workspace = Workspace.get(guid=workspace_id)

if workspace:
	if command == 'delete':
		workspace.delete()

self.hpt_main.htmlcode = TemplateWorkspaceCollection(Workspace.all()).html
