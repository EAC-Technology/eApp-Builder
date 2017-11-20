import json
from collections import OrderedDict
from class_plugins import Plugins

DEFAULT_MACRO_IMG  = "<img src='/b41299d0-b0bc-4d31-a320-ed5eb62568ca.png'/>"
DEFAULT_PLUGIN_IMG = "<img src='/abfbe7cf-76ac-46ba-9ba8-6c89933d7cae.png'/>"
DEFAULT_VDOM_CLASS_ID = "c9b2a813-7c02-4833-875c-9d260bf9b3b6"

CONFIG_MACRO_NAME = "config"


class WidgetMacros:

	def __init__( self ):
		self.pictures = []
		self.buttons = []

	def fetch_data( self, page_name ):

		plugins = Plugins.get_all()

		for plugin in plugins:

			board_macros_count = 0
			macros_on_page_count = 0
			for macros in plugin.get_macros():

				if 	macros.is_button_macros == "1" and \
								macros.page == page_name and \
								macros.name != CONFIG_MACRO_NAME:


					macros_on_page_count += 1

					if macros.on_board	!= "1": continue

					board_macros_count += 1

					if macros.macros_picture:
						self.pictures.append( macros.macros_picture )

					self.buttons.append({
						"guid"		: "m_" + macros.guid,
						"data"		: json.dumps({
										"name"		: macros.name,
										"picture"	: "<img src='/get_image?id=%s'/>" % macros.macros_picture if macros.macros_picture else DEFAULT_MACRO_IMG
									}),
						"position"	: macros.zindex,
						})

			if macros_on_page_count > board_macros_count:
				if plugin.picture:
					self.pictures.append( plugin.picture )

				self.buttons.append({
						"guid"		: "p_" + plugin.guid,
						"data"		: json.dumps({
										"name"		: plugin.name,
										"picture"	: "<img src='/get_image?id=%s'/>" % plugin.picture if plugin.picture else DEFAULT_PLUGIN_IMG
									}),
						"position"	: plugin.zindex,
						})

	def get_data( self ):
		return OrderedDict( [ ( item['guid'], item['data'] ) \
								for item in sorted( self.buttons, key = lambda k: k['position'] ) ] )


	def set_img( self ):
		from cStringIO import StringIO
		html_buffer = StringIO()
		html_buffer.write( "<div class='img-grid'>" )
		html_buffer.writelines( [ "<img src='/get_image?id=%s'/>" % pic_guid for pic_guid in self.pictures[:4] ] )
		html_buffer.write( "</div>" )
		return html_buffer.getvalue()



	def render(self, objectview, img_holder=None, header_button=None, page_name=None):
		self.fetch_data( page_name )
		if self.buttons:
			objectview.vdomclassid = DEFAULT_VDOM_CLASS_ID
			objectview.data = json.dumps( self.get_data() )
			if img_holder:	img_holder.htmlcode = self.set_img()
		else:
			header_button.visible = "0"

