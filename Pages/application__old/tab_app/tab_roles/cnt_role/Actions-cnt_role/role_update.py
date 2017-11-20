from models import Workspace, Role, Right
from forms import RoleCreateForm, RoleUpdateForm, RightCreateForm, RightUpdateForm

args = request.arguments

if 'workspace_id' not in args:
	raise Exception('Application ID is not provided')

workspace_id = args.get('workspace_id')
command = args.get('command', u'')
type = args.get('input_type', u'role').lower()
#raise Exception(str(', '.join([key+"="+args[key] for key in args])))

workspace = Workspace.get(guid=workspace_id)

if not workspace:
	self.action('goTo', ['/main'])

elif command in ['delete', 'update']:

	if 'object_id' not in args:
		raise Exception(u'Role ID is not provided')

	object_id = args['object_id']
	ObjectModel = Role if type == 'role' else Right
	instance = ObjectModel.get(guid=object_id, workspace_id=workspace.guid)

	if instance:
		if command == 'delete':
			instance.delete()
		else:
			ObjectForm = RoleUpdateForm if type == 'role' else RightUpdateForm
			form_update = ObjectForm(
				instance,
				name=args['title'],
				description=args['description'],
			)
			if form_update.is_valid():
				form_update.save()

		if command == 'delete' or not form_update.errors:
			self.dialog_update.action('hide', ['0'])
	else:
		self.action('goTo', ['/main'])

elif command == 'create':

	ObjectForm = RoleCreateForm if type == 'role' else RightCreateForm

	form_create = ObjectForm(
		name=args.get('title', ''),
		description=args['description'],
		workspace_id=workspace.guid
	)

	if form_create.is_valid():
		form_create.save()