import json
import cgi
import localization

class WidgetMacros:
	def __init__(self):
		self.__datatable = None
		self.__macros_list = None

	def set_data(self, data):
		macros = []
		for m in data:
			if m.name == "config":
				macros.append({ "id" : m.id,
					"Picture" : "<img src='/get_image?id="+m.macros_picture+"'/>" if m.macros_picture else "<img src='/b41299d0-b0bc-4d31-a320-ed5eb62568ca.png' />",
					"Macros_info" : "<h1>" + m.name + "</h1><p class='clearfix'></p><p>" + m.description + "</p><p></p>",
					"Edit_info" : "<div class='disabled_button'><a href=''><img src='/bfd88533-b697-4ce2-8a4f-ba85e269820b.res'/>Edit info</a></div>",
					"Edit_source" : "<a href=''><img src='/0820c4a6-73d6-4787-9afa-dccaf4582296.res'/>Edit source</a>",
					"Delete" : "<a href=''>Delete</a>"

				   })
			else:
				macros.append({ "id" : m.id,
					"Picture" : "<img src='/get_image?id="+m.macros_picture+"'/>" if m.macros_picture else "<img src='/b41299d0-b0bc-4d31-a320-ed5eb62568ca.png' />",
					"Macros_info" : "<h1>" + m.name + "</h1><p class='clearfix'></p><p>" + m.description + "</p><p></p>",
					"Edit_info" : "<a href=''><img src='/bfd88533-b697-4ce2-8a4f-ba85e269820b.res'/>Edit info</a>",
					"Edit_source" : "<a href=''><img src='/0820c4a6-73d6-4787-9afa-dccaf4582296.res'/>Edit source</a>",
					"Delete" : "<a href=''>Delete</a>"

				   })


		self.__macros_list = json.dumps(macros)

	def render(self, datatable):
		self.__datatable = datatable
		self.__datatable.data = self.__macros_list
