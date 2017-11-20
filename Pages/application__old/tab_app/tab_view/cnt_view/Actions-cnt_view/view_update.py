from models import Application, View
from forms import ViewCreateForm, ViewUpdateForm

args = request.arguments

error_objects = dict(
	name=self.dialog_update.form_update.tab_view_detail.tab_params.error_name,
)

if 'application_id' not in args:
	raise Exception('Application ID is not provided')

application_id = args.get('application_id')
command = args.get('command', u'')

app = Application.get(guid=application_id)

if not app:
	self.action('goTo', ['/main'])

elif command in ['delete', 'update']:

	if 'view_id' not in args:
		raise Exception(u'View ID is not provided')

	for error_key, error_object in error_objects.items():
		error_object.action('setText', [''])

	view_id = args['view_id']
	app_view = View.get(guid=view_id, application_id=app.guid)

	if app_view:
		form_update = ViewUpdateForm(app_view)

		if command == 'delete':
			app_view.delete()
		else:
			form_update = ViewUpdateForm(
				app_view,
				name=args['input_title'],
				layout_xml=args['input_layout_xml'],
				logic_xml=args['input_logic_xml'],
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
	form = ViewCreateForm(
		name=args.get('title', ''),
		application_id=app.guid
	)

	if form.is_valid():
		form.save()