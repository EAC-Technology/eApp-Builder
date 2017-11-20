"""
	Resource model
"""

import os.path
from utils_base_classes import SoftDeletionModel, cached_property
from model_application import Application
import base64


class Resource(SoftDeletionModel):

	db_table = 'eapp_resource'  # db_table
	fields_list = ['id', 'guid', 'application_id', 'name', 'file']
	guid_key = 'guid'  # will generate uuid automatically when created new row
	to_json_fields = ['guid', 'name', 'file_size']

	@cached_property
	def application(self):
		return Application.get(guid=self.application_id) if self.application_id else None

	@cached_property
	def file_path(self):
		return os.path.join(self.application.workspace_id, self.application_id, self.guid)

	@cached_property
	def file_size(self):
		return application.storage.getsize(self.file_path)

	@property
	def b64content(self):
		if not application.storage.exists(self.file_path):
			return None

		file = application.storage.open(self.file_path, "rb")
		content = file.read()
		file.close()
		return base64.b64encode(content)

	def save(self, file=None, b64content=None):
		super(Resource, self).save()

		# create folder after creation if not exists
		self.application.make_storage()

		# if file
		if file:
			application.storage.write(self.file_path, file.handler.read())
		elif b64content:
			file = application.storage.open(self.file_path, "wb")
			content = base64.b64decode(b64content)
			file.write(content)
			file.close()


	def delete(self):
		super(Resource, self).delete()

		# remove folder after deletion
		if application.storage.exists(self.file_path):
			application.storage.delete(self.file_path)





