from models import Workspace, Widget

widget_id = request.arguments.get('widget_id', '')
command = request.arguments.get('command', 'update')

widget = Widget.get(guid=widget_id)

if widget:
	disabled = '2' if command == 'delete' else '0'

	form = self.dialog_update.form_update
	form.title.value = widget.name
	form.title.mode = disabled

	form.workspace_id.value = widget.workspace_id
	form.widget_id.value = widget.guid
	form.command.value = command
	self.dialog_update.form_update.btn_update.label = command.title()
	form.btn_update.action( "setLabel", [ command.title() ] )
	form.btn_update.action( "setClass", [ 'btn btn-danger' if command == 'delete' else 'btn btn-success' ] )
	self.dialog_update.title = 'Widget {}'.format(command.title())
	self.dialog_update.show = '1'
