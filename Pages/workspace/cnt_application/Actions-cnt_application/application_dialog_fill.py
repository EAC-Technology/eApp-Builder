from models import Application

application_id = request.arguments.get('application_id', '')
command = request.arguments.get('command', 'update')

app = Application.get(guid=application_id)

if app:
	disabled = '2' if command == 'delete' else '0'

	form = self.dialog_update.form_update
	form.title.value = app.name
	form.title.mode = disabled

	form.workspace_id.value = app.workspace_id
	form.application_id.value = app.guid
	form.command.value = command
	self.dialog_update.form_update.btn_update.label = command.title()
	form.btn_update.action( "setLabel", [ command.title() ] )
	form.btn_update.action( "setClass", [ 'btn btn-danger' if command == 'delete' else 'btn btn-success' ] )
	self.dialog_update.title = 'Application {}'.format(command.title())
	self.dialog_update.show = '1'
