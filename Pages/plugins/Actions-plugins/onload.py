from widget_user_group_dialog import authenticated, error_handler, administrator, license_confirmed

@license_confirmed
@authenticated
@administrator
@error_handler
def main():

	import json, localization, base64
	from xml.dom.minidom import parseString
	from class_macro import Macros
	from class_plugins import Plugins
	from class_timer import Timer
	from class_custom_event import CustomEvent
	from class_xml_macro import XMLMacros
	from class_xml_timer import XMLTimer
	from class_xml_custom_event import XMLCustomEvent
	from class_xml_plugin import XMLPlugin
	from class_xml_plugin_db import XMLPluginDB
	from class_xml_resource import XMLResource
	from utils.uuid import uuid4
	from widget_localization import LocalizationWidget
	from widget_plugins import WidgetPlugins
	from VEE_resources import create_plugin_dir, ResourceFolderManager
	from VEE_sqlite3 import DatabaseManager

	lang = localization.get_lang()

	if "formbutton_save_plugin" in request.arguments:
		plugin = Plugins()
		plugin.guid = str(uuid4())
		plugin.name = request.arguments.get("formtext_name", "")
		plugin.author = request.arguments.get("formtext_author", "")
		plugin.description = request.arguments.get("formtextarea_description", "")
		plugin.version = request.arguments.get("formtext_version", "")
		plugin.zindex = "1"

		if "uploader" in request.arguments:
			file = request.arguments.get("uploader", "", castto=Attachment)
			if file:
				plugin.picture = str(uuid4())
				application.storage.write(plugin.picture, file.handler.read())

		plugin.save()
		create_plugin_dir(plugin.guid)

	if "formbutton_upload_plugin" in request.arguments:
		if request.arguments.get("uploader", "", castto=Attachment):
			try:
				file = request.arguments.get("uploader", "", castto=Attachment)
				xml_data = file.handler.read()

				dom = parseString( xml_data)
				node = XMLPlugin( dom )

				if not Plugins.get_by_guid(node.guid):
					plugin = Plugins()
					plugin.name = node.name
					plugin.description = node.description
					plugin.guid = node.guid
					plugin.version = node.version
					plugin.author = node.author
					plugin.protected = node.protected

					plugin_picture_name = ""
					plugin.picture = ""
					if node.picture:
						plugin.picture = plugin_picture_name = str(uuid4())
						application.storage.write(plugin_picture_name, base64.b64decode(node.picture))
					plugin.save()
					create_plugin_dir(plugin.guid)


					for child in node.childs:

						if child.tag == "timer":
							child = XMLTimer( child )

							if child.name:
								timer = Timer()
								timer.fill_from_xml(child, node.guid)
						elif child.tag == "custom_event":
							child = XMLCustomEvent( child )

							if child.name:
								custom_event = CustomEvent()
								custom_event.fill_from_xml(child, node.guid)
						elif child.tag == "macro":
							child = XMLMacros( child )
							if child.name and child.source:
								macros = Macros()
								macros.fill_from_xml(child, node.guid)
						elif child.tag == "database":
							child = XMLPluginDB( child )
							if child.name:
								DatabaseManager(plugin.guid).import_db(child.name, base64.b64decode(child.db_source))
						elif child.tag == "resource":
							child = XMLResource( child )

							if child.name:
								ResourceFolderManager(plugin.guid).import_res(child.name, base64.b64decode(child.res_source))
						else:
							raise Exception(lang.get("xml_not_correctr_error","xml_not_correctr_error"))
				else:
					raise Exception(lang.get("plugin_exist","plugin_exist"))

			except Exception, ex:
				self.growl.title = lang["error"]
				self.growl.text = ex
				self.growl.show = "1"


	if "formbutton_import" in request.arguments:
		if request.arguments.get("uploader", "", castto=Attachment):
			file = request.arguments.get("uploader", "", castto=Attachment)
			xml_data = file.handler.read()
			dom = parseString( xml_data)
			node = XMLMacros( dom )

			for child in node.childs:
				child = XMLMacros( child )
				if child.name and child.source:
					macros = Macros()
					macros.name 			= child.name
					macros.code 			= child.source
					macros.class_name		= child.class_name
					macros.is_button_macros = child.is_button
					macros.on_board 		= child.on_board

					picture_name = ""
					macros.macros_picture = ""
					if child.macros_picture:
						macros.macros_picture = picture_name = str(uuid4())
						application.storage.write(picture_name, base64.b64decode(child.macros_picture))

					macros.save()
				else:
					self.growl.title = lang["error"]
					self.growl.text	= lang["xml_not_correctr_error"]
					self.growl.visible = "1"

	if "op" in request.arguments and request.arguments.get("op") == "export":
		plugin = Plugins.get_by_id(session.get("plugin_id", ""))
		output = plugin.export()
		output_len = output.tell()
		output.seek(0)
		response.send_file( plugin.name.encode( 'utf8' ) + ".xml", output_len, output )

	if "formtext_pluginid" in request.arguments:
		args = request.arguments
		plugin = Plugins.get_by_id( args.get( "formtext_pluginid", "" ) )
		file = request.arguments.get("uploader", "", castto=Attachment)

		if plugin and file:

			xml_data = file.handler.read()
			dom = parseString( xml_data)
			node = XMLPlugin( dom )

			new_plugin 				= Plugins()
			new_plugin.name 		= node.name
			new_plugin.description 	= node.description
			new_plugin.guid 		= node.guid
			new_plugin.version 		= node.version
			new_plugin.author 		= node.author
			new_plugin.protected	= node.protected

			err_msg = None
			if plugin.guid != new_plugin.guid:
				err_msg = "Wrong guid"

			elif plugin.version > new_plugin.version:
				err_msg = "The update that you are trying to install has older version than installed plugin"

			if err_msg:
				self.dialog_error.text_description.value = err_msg
				self.dialog_error.show = "1"
				self.dialog_update_plugin.text_description.value = self.dialog_update_plugin.text_description.value % ( plugin.name )
				self.dialog_update_plugin.form.formtext_pluginid.value = plugin.id
				self.dialog_update_plugin.show = "1"


			else:

				if plugin.picture:
					application.storage.delete( plugin.picture )
				plugin.delete(True)

				new_plugin.picture = ""
				if node.picture:
					new_plugin.picture = str(uuid4())
					application.storage.write( new_plugin.picture, base64.b64decode(node.picture))

				new_plugin.save()

				for child in node.childs:
					if child.tag == "macro":
						child = XMLMacros( child )

						if child.name and child.source:
							macros = Macros()
							macros.fill_from_xml(child, node.guid)
					elif child.tag == "timer":
						child = XMLTimer( child )

						if child.name:
							timer = Timer()
							timer.fill_from_xml(child, node.guid)
					elif child.tag == "custom_event":
						child = XMLCustomEvent( child )

						if child.name:
							custom_event = CustomEvent()
							custom_event.fill_from_xml(child, node.guid)
					elif child.tag == "database":
						child = XMLPluginDB( child )
						if child.name:
							DatabaseManager(new_plugin.guid).import_db(child.name, base64.b64decode(child.db_source))
					elif child.tag == "resource":
						child = XMLResource( child )

						if child.name:
							ResourceFolderManager(new_plugin.guid).import_res(child.name, base64.b64decode(child.res_source))
					else:
						self.growl.title = lang["error"]
						self.growl.text	= lang["xml_not_correctr_error"]
						self.growl.visible = "1"


	widget_plugins = WidgetPlugins()
	plugins_obj = Plugins.get_all()
	widget_plugins.set_data(plugins_obj)
	widget_plugins.render(self.datatable_plugin)
#	localization_wdgt = LocalizationWidget()
#
#	localization_wdgt.add_controls( "dialog_uninstall_plugin_title", self.dialog_uninstall )
#	localization_wdgt.add_controls( "btn_upload_files", self.dialog_uninstall.button_apply )
#	localization_wdgt.add_controls( "btn_new_folder", self.dialog_uninstall.button_cancel )
#	localization_wdgt.add_controls( "dialog_uninstall_plugin_text", self.dialog_uninstall.text_uninstall )
#
#	localization_wdgt.render()




main()
