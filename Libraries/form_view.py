from models import View
from utils_base_classes import ModelForm


class ViewCreateForm(ModelForm):

	model = View
	mandatory = ['name']


class ViewUpdateForm(ModelForm):

	model = View
	mandatory = ['name']

