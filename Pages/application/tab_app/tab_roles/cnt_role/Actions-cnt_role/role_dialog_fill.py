from models import Role, Right

object_id = request.arguments.get('object_id', '')
type = request.arguments.get('type', 'role')  # or 'right'
command = request.arguments.get('command', 'update')

object_instance = Role.get(guid=object_id) if type == 'role' else Right.get(guid=object_id)

if object_instance:
	disabled = '2' if command == 'delete' else '0'

	form = self.dialog_update.form_update

	form.title.value = object_instance.name
	form.title.mode = disabled
	form.description.value = object_instance.description
	form.description.mode = disabled
	form.command.value = command
	form.object_id.value = object_instance.guid
	form.workspace_id.value = object_instance.workspace_id

	self.dialog_update.form_update.btn_update.label = command.title()
	form.btn_update.action( "setClass", [ 'btn btn-danger' if command == 'delete' else 'btn btn-success' ] )
	self.dialog_update.title = '{} {}'.format(type.title(), command.title())
	self.dialog_update.show = '1'
