import json

class WidgetPluginDB:
	def __init__(self):
		self.__datatable = None
		self.__db_list = None

	def set_data(self, data):
		plugin_db = [{"id": db,
					"Picture" : "<img src='0b4d0a39-487e-4954-9293-ef467ed727e7.res' />",
					"Name" : "<h1>" + db + "</h1>",
					"Import" : "<a href=''><img src='/7452291d-f0c0-444c-997f-ba3064ddc0c7.res'/>Update</a>",
					"Export" : "<a href=''><img src='/cb4d01af-36f7-418d-94d8-e8a0546e5877.res'/>Download</a>",
					"Delete" : "<a href=''>Delete</a>"} for db in data]

		self.__db_list = json.dumps(plugin_db)

	def render(self, datatable = None):
		if datatable:
			self.__datatable = datatable
			self.__datatable.data = self.__db_list
