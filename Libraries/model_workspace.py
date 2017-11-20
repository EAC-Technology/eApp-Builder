"""
	Main model to regroup different eapp projects (applications, widgets, data sources).
"""

import os
from utils_base_classes import SoftDeletionModel


class Workspace(SoftDeletionModel):

	db_table = 'eapp_workspace'  # db_table
	fields_list = ['id', 'guid', 'name', 'description']
	guid_key = 'guid'  # will generate uuid automatically when created new row
	to_json_fields = ['guid', 'name', 'description']
	to_json_childs = ["applications", "widgets", "data_sources"]

	def __str__(self):
		return '%(name)s (%(id)s)%(deleted)s' % {
			'name': self.name,
			'id': self.id,
			'deleted': '[X]' if self.is_deleted else ''
		}

	@property
	def widgets(self):
		from model_widget import Widget
		return Widget.filter(workspace_id=self.guid)

	@property
	def applications(self):
		from model_application import Application
		return Application.filter(workspace_id=self.guid)

	@property
	def data_sources(self):
		from model_data_source import DataSource
		return DataSource.filter(workspace_id=self.guid)

	@property
	def roles(self):
		from model_acl import Role
		return Role.filter(workspace_id=self.guid)

	@property
	def rights(self):
		from model_acl import Right
		return Right.filter(workspace_id=self.guid)

	def make_storage(self):
		# create folder after creation if not exists
		workspace_path = os.path.join('workspaces', self.guid)
		if not application.storage.exists(workspace_path):
			if not application.storage.exists('workspaces'):
				application.storage.mkdir('workspaces')
			application.storage.mkdir(self.guid)

	def save(self):
		super(Workspace, self).save()
		self.make_storage()

	def delete(self):
		for widget in self.widgets:
			widget.delete()

		for app in self.applications:
			app.delete()

		for data_source in self.data_sources:
			data_source.delete()

		for role in self.roles:
			role.delete()

		for right in self.rights:
			right.delete()

		super(Workspace, self).delete()

		# remove folder after deletion
		if application.storage.exists(self.guid):
			application.storage.delete(self.guid)


