from models import Workspace

workspace_id = request.arguments.get('workspace_id', '')
command = request.arguments.get('command', 'update')

workspace = Workspace.get(guid=workspace_id)

if workspace:
	disabled = '2' if command == 'delete' else '0'

	form = self.dialog_update.form_update
	form.title.value = workspace.name
	form.description.value = workspace.description
	form.workspace_id.value = workspace.guid
	form.title.mode = disabled
	form.description.mode = disabled
	form.command.value = command
	self.dialog_update.form_update.btn_update.label = command.title()
	form.btn_update.action( "setLabel", [ command.title() ] )
	form.btn_update.action( "setClass", [ 'btn btn-danger' if command == 'delete' else 'btn btn-success' ] )
	self.dialog_update.title = 'Workspace {}'.format(command.title())
	self.dialog_update.show = '1'
