from forms import ApplicationParametersForm

error_objects = dict(
	name=self.form_params.error_name,
	description=self.form_params.error_description,
	author=self.form_params.error_author,
	version=self.form_params.error_version,
)

args = request.arguments
input_data = dict(
	author=args.get('input_author', ''),
	params=dict(
		autoincrement=bool(args.get('input_autoincrement', False)),
		license=bool(args.get('input_license', False)),
	),
	description=args.get('input_description', ''),
	name=args.get('input_name', ''),
	version=args.get('input_version', ''),
)

# always clean all error messages first
for error_key, error_object in error_objects.items():
	error_object.action('setText', [''])

form = ApplicationParametersForm(instance_id=args.get('input_id', ''), **input_data)

if form.is_valid():
	form.save()

	self.form_params.hpt_status.action('show', [''])
	self.form_params.hpt_status.action('setHTML', ['<div class="text-muted">Successfully updated</div>'])
	self.form_params.hpt_status.action('hide', ['3000'])

else:
	self.form_params.hpt_status.action('show', [''])
	self.form_params.hpt_status.action('setHTML', ['<div class="text-danger">Errors found!</div>'])

	for error_key, error_object in error_objects.items():
		if error_key in form.errors:
			error_object.action('setText', [', '.join(form.errors[error_key])])

