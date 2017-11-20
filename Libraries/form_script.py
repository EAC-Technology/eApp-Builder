from models import AppScript
from utils_base_classes import ModelForm


class AppScriptCreateForm(ModelForm):

	model = AppScript
	mandatory = ['name']


class AppScriptUpdateForm(ModelForm):

	model = AppScript
	mandatory = ['name']

