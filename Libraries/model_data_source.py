"""
	Data Source model
"""

from utils_base_classes import SoftDeletionModel
from model_workspace import Workspace


class DataSource(SoftDeletionModel):

	db_table = 'eapp_data_source'  # db_table
	fields_list = ['id', 'guid', 'workspace_id', 'connector']
	guid_key = 'guid'  # will generate uuid automatically when created new row

	to_json_fields = ['guid', 'name']

	def __str__(self):
		return '%(name)s (%(id)s)%(deleted)s' % {
			'name': self.name,
			'id': self.id,
			'deleted': '[X]' if self.is_deleted else ''
		}

	@property
	def name(self):
		return 'data_source_{}'.format(self.id)

	@property
	def workspace(self):
		return Workspace.get(guid=self.workspace_id) if self.workspace_id else None


