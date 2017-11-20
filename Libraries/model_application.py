"""
	Application model
"""
import os
import json

from utils_base_classes import SoftDeletionModel, cached_property
from model_workspace import Workspace


class Application(SoftDeletionModel):

	db_table = 'eapp_application'  # db_table
	fields_list = [
		'id', 'guid', 'workspace_id', 'creator_id', 'start_view_id',
		'name', 'description', 'version', 'author', 'params', 'icon']
	guid_key = 'guid'  # will generate uuid automatically when created new row
	json_fields = {'params': ('license', 'autoincrement')}

	to_json_fields = [ 'guid', 'creator_id', 'start_view_id', 'name', 'description', 'version', 'author', 'params', 'icon']
	to_json_childs = ["views", "resources"]

	@cached_property
	def workspace(self):
		return Workspace.get(guid=self.workspace_id) if self.workspace_id else None

	@property
	def views(self):
		from model_view import View
		return View.filter(application_id=self.guid)

	@property
	def resources(self):
		from model_resource import Resource
		return Resource.filter(application_id=self.guid)

	@property
	def roles(self):
		from model_acl import Role
		return Role.filter(workspace_id=self.workspace_id)

	@property
	def scripts(self):
		from model_script import AppScript
		return AppScript.filter(application_id=self.guid)

	@property
	def start_view(self):
		from model_view import View
		return View.get(guid=self.start_view_id) if self.start_view_id else None

	@property
	def license(self):
		return bool(self.params.get('license', False))

	@license.setter
	def license(self, value):
		self.params['license'] = True if bool(value) else False

	@property
	def autoincrement(self):
		return bool(self.params.get('autoincrement', True))

	@autoincrement.setter
	def autoincrement(self, value):
		self.params['autoincrement'] = True if bool(value) else False

	def make_storage(self):
		# create folder after creation if not exists
		app_resource_path = os.path.join(self.workspace_id, self.guid)
		if not application.storage.exists(app_resource_path):
			self.workspace.make_storage()
			application.storage.mkdir(app_resource_path)

	def save(self):
		super(Application, self).save()
		self.make_storage()

	def delete(self):
		for view in self.views:
			view.delete()

		for resource in self.resources:
			resource.delete()

		super(Application, self).delete()

		# remove folder after deletion
		app_resource_path = os.path.join(self.workspace_id, self.guid)
		if application.storage.exists(app_resource_path):
			application.storage.delete(app_resource_path)



