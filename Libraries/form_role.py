from models import Role, Right
from utils_base_classes import ModelForm


class RoleCreateForm(ModelForm):

	model = Role
	mandatory = ['name']


class RoleUpdateForm(ModelForm):

	model = Role
	mandatory = ['name']


class RightCreateForm(ModelForm):

	model = Right
	mandatory = ['name']


class RightUpdateForm(ModelForm):

	model = Right
	mandatory = ['name']

