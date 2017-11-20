import json
from VEE_resources import ResourceFolderManager
import mimetypes


class WidgetResource:
	def __init__(self):
		self.__datatable = None
		self.__resource_list = None

	def set_data(self, data, plugin_guid):
		resources = []
		for res in data:
			mimetype = mimetypes.guess_type( res, strict=False )[0]
			resources.append({"id": res,
					"Picture" : "<img src='" + ResourceFolderManager(plugin_guid).public_link( res ) + "' />" if mimetype and "image" in mimetype else "<img src='358b703e-65e9-4a71-ab7f-e1bab238f027.res' />",
					"Name" : res,
					"Export" : "",
					"Delete" : "<a href=''>Delete</a>"})
		self.__resource_list = json.dumps(resources)

	def render(self, datatable = None):
		if datatable:
			self.__datatable = datatable
			self.__datatable.data = self.__resource_list
