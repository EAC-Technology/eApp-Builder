from models import Application
from utils_base_classes import ModelForm


class ApplicationParametersForm(ModelForm):

	model = Application
	mandatory = ['name', 'author']

	def clean(self):
		super(ApplicationParametersForm, self).clean()

		filtered = Application.filter(workspace_id=self.instance.workspace_id, name=self.fields['name'])
		if filtered and filtered[0].id != self.instance.id:
			self.errors['name'].append("Application with this name already exists")


class ApplicationCreate(ModelForm):

	model = Application
	mandatory = ['name', 'workspace_id']
	fields_list = ['name', 'workspace_id']

	def clean(self):
		super(ApplicationCreate, self).clean()

		filtered = Application.filter(workspace_id=self.instance.workspace_id, name=self.fields['name'])
		if filtered and filtered[0].id != self.instance.id:
			self.errors['name'].append("Application with this name already exists")
