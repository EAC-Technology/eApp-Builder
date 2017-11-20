from models import Application, Workspace
from forms import ApplicationCreate

args = request.arguments

if 'workspace_id' not in args:
	raise Exception('Workspace ID is not provided')

workspace_id = args.get('workspace_id')
command = args.get('command', u'')

workspace = Workspace.get(guid=workspace_id)

if not workspace:
	self.action('goTo', ['/main'])

elif command in ['delete', 'update']:

	if 'application_id' not in args:
		raise Exception(u'Application ID is not provided')
	application_id = args['application_id']
	app = Application.get(guid=application_id, workspace_id=workspace.guid)

	if app:
		if command == 'delete':
			app.delete()
		else:
			title = args['title']
			if title:
				app.name = title
				app.save()

	self.dialog_update.action('hide', ['0'])

elif command == 'create':
	form = ApplicationCreate(
		name=args.get('title', ''),
		workspace_id=workspace.guid
	)

	if form.is_valid():
		form.save()
