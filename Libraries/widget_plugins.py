import json
import cgi
import localization
from class_macro import Macros

class WidgetPlugins:
	def __init__(self):
		self.__datatable = None
		self.__richtext = None
		self.__plugins_list = None
		self.__richtext_value = None

	def set_data(self, data):
		plugins = []
		for plugin in data:
			config_macros = Macros.get_config_macro(plugin.guid)
			plugins.append({"id": plugin.id,
					"Picture" : "<img src='/get_image?id="+plugin.picture+"' width='48'/>" if plugin.picture else "<img src='/abfbe7cf-76ac-46ba-9ba8-6c89933d7cae.png' />",
					"Plugin_info" : "<h1>" +plugin.name + "</h1><h2>by " + plugin.author + "</h2><p class='clearfix'></p><p>" + plugin.description + "</p><p>Version " + plugin.version + "</p>",
					"Update" : "<a href=''><img src='/7452291d-f0c0-444c-997f-ba3064ddc0c7.res'/>Update</a>",
					"Export" : "<a href=''><img src='/cb4d01af-36f7-418d-94d8-e8a0546e5877.res'/>Export</a>",
					"Open" : "<a href=''><img src='/3827f2ea-edca-491a-bc5f-a765776dd109.res'/>Open</a>",
					"Delete" : "<a href=''>Uninstall</a>",
					"MD5" : "<a href=''>Get MD5</a>",
					"Config" : ("<a href=''>Config</a>" if config_macros else "")} if not plugin.protected else {"id": plugin.id,
					"Picture" : "<img src='/get_image?id="+plugin.picture+"' width='48'/>" if plugin.picture else "<img src='/abfbe7cf-76ac-46ba-9ba8-6c89933d7cae.png' />",
					"Plugin_info" : "<h1>" +plugin.name + "</h1><h2>by " + plugin.author + "</h2><p class='clearfix'></p><p>" + plugin.description + "</p><p>Version " + plugin.version + "</p><p>Protected</p>" ,
					"Update" : "<a href=''><img src='/7452291d-f0c0-444c-997f-ba3064ddc0c7.res'/>Update</a>",
					"Export" : "",
					"Open" : "",
					"Delete" : "<a href=''>Uninstall</a>",
					"MD5" : "<a href=''>Get MD5</a>",
					"Config" : ("<a href=''>Config</a>" if config_macros else "")})

		self.__plugins_list = json.dumps(plugins)

	def set_single_data(self, data):

#		plugins = [{"id": data.id,
#					"Picture" : "<img src='/get_image?id=" +data.picture+ "'/>" if data.picture else "<img src='/abfbe7cf-76ac-46ba-9ba8-6c89933d7cae.png'/>",
#					"Plugin_info" : "<h1>" + data.name + "</h1><h2>by " + data.author + "</h2><p class='clearfix'></p><p>" + data.description + "</p><p>Version " + data.version + "</p>",
#					"Update" : "<a href='?op=update&id=" + str(data.id) + "'><img src='/7452291d-f0c0-444c-997f-ba3064ddc0c7.res'/>Update</a>",
#					"Export" : "<a href='?op=export&id=" + str(data.id) + "'><img src='/cb4d01af-36f7-418d-94d8-e8a0546e5877.res'/>Export</a>",
#					"Open" : "<a href='?op=edit&id=" + str(data.id) + "'><img src='/bfd88533-b697-4ce2-8a4f-ba85e269820b.res'/>Edit Details</a>"}]
#
		img = "<img src='/get_image?id=" +data.picture+ "' width='48'/>" if data.picture else "<img src='/abfbe7cf-76ac-46ba-9ba8-6c89933d7cae.png'/>"
		self.__richtext_value =  img + "<h1>" + data.name + "</h1><h2>by " + data.author + "</h2><p class='clearfix'></p>" \
		"<div class='breadcrumbs'><a href='/plugins.vdom'>Plug-Ins</a> > " + data.name + "</div>"
		#self.__plugins_list = json.dumps(plugins)


	def render(self, datatable = None, richtext = None):
		if datatable:
			self.__datatable = datatable
			self.__datatable.data = self.__plugins_list
		if 	richtext:
			self.__richtext = richtext
			self.__richtext.value = self.__richtext_value
