"""
	Script model for eApp
"""

import os.path
from utils_base_classes import SoftDeletionModel, cached_property
from model_application import Application


class AppScript(SoftDeletionModel):

	db_table = 'eapp_script'  # db_table
	fields_list = ['id', 'guid', 'name', 'application_id', 'source']
	guid_key = 'guid'  # will generate uuid automatically when created new row

	@cached_property
	def application(self):
		return Application.get(guid=self.application_id) if self.application_id else None

