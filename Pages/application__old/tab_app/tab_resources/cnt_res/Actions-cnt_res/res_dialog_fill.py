from models import Resource

res_id = request.arguments.get('res_id', '')
command = request.arguments.get('command', 'update')

instance = Resource.get(guid=res_id)

if instance:
	disabled = '2' if command == 'delete' else '0'

	form = self.dialog_update.form_update
	self.dialog_update.form_update.res_upload.value = instance.name
	self.dialog_update.form_update.res_upload.mode = disabled
	form.command.value = command
	form.res_id.value = instance.guid
	form.application_id.value = instance.application_id
	form.btn_update.action( "setClass", [ 'btn btn-danger' if command == 'delete' else 'btn btn-success' ] )

	self.dialog_update.form_update.btn_update.label = command.title()
	self.dialog_update.title = 'Resource {}'.format(command.title())
	self.dialog_update.show = '1'