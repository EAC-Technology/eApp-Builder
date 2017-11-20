from models import Application

app_id = request.arguments.get('id', '')
app = Application.get(guid=app_id)
if app:

	# Parameters tab
	self.form_params.input_author.value = app.author or ''
	self.form_params.input_description.value = app.description or ''
	self.form_params.input_guid.value = app.guid
	self.form_params.input_autoincrement.state = app.autoincrement
	self.form_params.input_license.state = app.license
	self.form_params.input_name.value = app.name or ''
	self.form_params.input_version.value = app.version
	self.form_params.input_id.value = app.id

	self.form_params.error_name.value = ''
	self.form_params.error_description.value = ''
	self.form_params.error_version.value = ''
	self.form_params.error_author.value = ''