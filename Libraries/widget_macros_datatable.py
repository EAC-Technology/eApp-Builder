import json
from class_plugins import Plugins

CONFIG_MACRO_NAME = "config"
class WidgetMacrosDatatable( object ):

	def __init__( self, plugin_guid, page_name = None  ):
		self.page_name 		= page_name
		self.plugin_guid 	= plugin_guid

	def render( self, datatable, dialog ):

		plugin = Plugins.get_by_guid( self.plugin_guid )
		if not plugin:
			raise Exception( "Plugin with GUID={guid} doesn't exists".format( \
										guid = self.plugin_guid ) )

		data = []
		for macro in plugin.get_macros():
			if 	macro.on_board != "1" and \
					macro.is_button_macros == "1" and \
					macro.page == self.page_name and \
					macro.name != CONFIG_MACRO_NAME:

				data.append( (
					macro.guid,
					"<img src='/get_image?id=%s'/>"%macro.macros_picture if macro.macros_picture else "",
					macro.name
				) )

		datatable.data 	= json.dumps( data )
		dialog.title	= plugin.name





