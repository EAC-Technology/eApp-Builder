from models import DataSource

data_source_id = request.arguments.get('data_source_id', '')
command = request.arguments.get('command', 'update')

data_source = DataSource.get(guid=data_source_id)

if data_source:
	disabled = '2' if command == 'delete' else '0'

	form = self.dialog_update.form_update
	form.connector.value = data_source.connector
	form.connector.mode = disabled

	form.workspace_id.value = data_source.workspace_id
	form.data_source_id.value = data_source.guid
	form.command.value = command
	self.dialog_update.form_update.btn_update.label = command.title()
	form.btn_update.action( "setLabel", [ command.title() ] )
	form.btn_update.action( "setClass", [ 'btn btn-danger' if command == 'delete' else 'btn btn-success' ] )
	self.dialog_update.title = 'Data Source {}'.format(command.title())
	self.dialog_update.show = '1'
