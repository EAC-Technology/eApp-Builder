from models import Application, AppScript
from forms import AppScriptCreateForm, AppScriptUpdateForm

args = request.arguments

error_objects = dict(
	name=self.dialog_update.form_update.tab_script_detail.tab_params.error_name,
)

if 'application_id' not in args:
	raise Exception('Application ID is not provided')

application_id = args.get('application_id')
command = args.get('command', u'')

app = Application.get(guid=application_id)

if not app:
	self.action('goTo', ['/main'])

elif command in ['delete', 'update']:

	if 'script_id' not in args:
		raise Exception(u'Script ID is not provided')

	for error_key, error_object in error_objects.items():
		error_object.action('setText', [''])

	script_id = args['script_id']
	app_script = AppScript.get(guid=script_id, application_id=app.guid)

	if app_script:
		form_update = AppScriptUpdateForm(app_script)

		if command == 'delete':
			app_script.delete()
		else:
			form_update = AppScriptUpdateForm(
				app_script,
				name=args['input_title'],
				source=args['input_source'],
			)
			if form_update.is_valid():
				form_update.save()
			else:
				for error_key, error_object in error_objects.items():
					if error_key in form_update.errors:
						error_object.action('setText', [', '.join(form_update.errors[error_key])])

		if not form_update.errors:
			self.dialog_update.action('hide', ['0'])
	else:
		self.action('goTo', ['/main'])

elif command == 'create':
	form = AppScriptCreateForm(
		name=args.get('title', ''),
		application_id=app.guid
	)

	if form.is_valid():
		form.save()
