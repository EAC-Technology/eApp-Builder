import shutil
import managers
import json
from models import Resource, Application
#from forms import RoleCreateForm, RoleUpdateForm, RightCreateForm, RightUpdateForm

args = request.arguments

if 'application_id' not in args:
	raise Exception('Application ID is not provided')

app_id = args.get('application_id')
command = args.get('command', u'')

app = Application.get(guid=app_id)

if not app:
	self.action('goTo', ['/main'])

elif command in ['delete', 'update']:

	if 'res_id' not in args:
		raise Exception(u'Res ID is not provided')

	object_id = args.get('res_id')
	instance = Resource.get(guid=object_id, application_id=app.guid)

	if instance:
		if command == 'delete':
			instance.delete()
		else:
			uploaded_file_id = args.get('res_file_id', "  ")  # todo: it's file, need to rename argument

			files = managers.session_manager.current.files or {}
			file_obj = Attachment(files.get(uploaded_file_id))

			if file_obj:
				instance.save(file_obj)  # save resource and copy the file

				file_obj.remove()

		self.dialog_update.action('hide', ['0'])
	else:
		self.action('goTo', ['/main'])

elif command == 'create':
	if 'res_file_id' not in args:
		raise Exception(u'Res ID is not provided')

	uploaded_file_id = args['res_file_id']  # todo: it's file, need to rename argument

	files = managers.session_manager.current.files or {}
	file_obj = Attachment(files.get(uploaded_file_id))

	if file_obj:
		res_object = Resource(application_id=app_id, name=file_obj.name)
		res_object.save(file_obj)  # save resource and copy the file

		file_obj.remove()  # remove temp file

	self.dialog_create.action('hide', ['0'])
