from widget_user_group_dialog import authenticated, error_handler, administrator, license_confirmed

@license_confirmed
@authenticated
@administrator
@error_handler
def main():

	import json, localization, base64
	from xml.dom.minidom import parseString
	from class_plugins import Plugins
	from class_xml_macro import XMLMacros
	from class_xml_timer import XMLTimer
	from class_xml_custom_event import XMLCustomEvent
	from class_xml_plugin import XMLPlugin
	from class_xml_plugin_db import XMLPluginDB
	from class_xml_resource import XMLResource
	from utils.uuid import uuid4
	from widget_localization import LocalizationWidget
	from widget_plugins import WidgetPlugins
	from widget_macro import WidgetMacros
	from widget_timer import WidgetTimer
	from widget_custom_event import WidgetCustomEvent
	from widget_plugin_db import WidgetPluginDB
	from widget_resource import WidgetResource
	from class_macro import Macros
	from class_timer import Timer
	from class_custom_event import CustomEvent
	from VEE_sqlite3 import DatabaseManager
	from VEE_resources import ResourceFolderManager

	lang = localization.get_lang()

	if "id" in request.arguments:
		try:
			plugin = Plugins.get_by_id(int(request.arguments.get("id", 0)))
			if plugin.protected:
				response.redirect("/plugins.vdom")
			macros = plugin.get_macros()
			timer_list = plugin.get_timer()
			custom_event_list = plugin.get_custom_event()

			config_is_exist = False
			for m in macros:
				if m.name == "config":
					config_is_exist = True

			if config_is_exist == True:
				self.button_config.visible = "1"
				self.button_create_config.visible = "0"
			else:
				self.button_config.visible = "0"
				self.button_create_config.visible = "1"

			response.shared_variables["plugin_id"] = plugin.id
			widget_plugins = WidgetPlugins()
			widget_plugins.set_single_data(plugin)
			widget_plugins.render(richtext = self.richtext_plugin)

			widget_macros = WidgetMacros()
			widget_macros.set_data(macros)
			widget_macros.render(self.datatable_macros)

			widget_timer = WidgetTimer()
			widget_timer.set_data(timer_list)
			widget_timer.render(self.datatable_timer)

			widget_custom_event = WidgetCustomEvent()
			widget_custom_event.set_data(custom_event_list)
			widget_custom_event.render(self.datatable_custom_event)

			widget_db = WidgetPluginDB()
			widget_db.set_data(DatabaseManager(plugin.guid).databaselist)
			widget_db.render(self.datatable_db)

			widget_resource = WidgetResource()
			widget_resource.set_data(ResourceFolderManager(plugin.guid).resourcelist, plugin.guid)
			widget_resource.render(self.datatable_resource)

			self.dialog_add_timer.action("hide", [])
		except Exception, ex:
			self.growl.title = lang["error"]
			self.growl.text	= str(ex)
			self.growl.visible = "1"



	if "formbutton_save_plugin" in request.arguments:
		plugin = Plugins.get_by_id(request.arguments.get("formtext_id", ""))
		if plugin:
			plugin.name = request.arguments.get("formtext_name", "")
			plugin.author = request.arguments.get("formtext_author", "")
			plugin.description = request.arguments.get("formtextarea_description", "")
			plugin.version = request.arguments.get("formtext_version", "")
			#raise Exception(file.name)
			if "uploader" in request.arguments:
				file = request.arguments.get("uploader", "", castto=Attachment)
				if file:
					plugin.picture = str(uuid4())
					application.storage.write(plugin.picture, file.handler.read())

			plugin.save()
		plugin = Plugins.get_by_id(int(request.arguments.get("formtext_id", "")))
		widget_plugins = WidgetPlugins()
		widget_plugins.set_single_data(plugin)
		widget_plugins.render(richtext = self.richtext_plugin)

		macros = plugin.get_macros()
		config_is_exist = False
		for m in macros:
			if m.name == "config":
				config_is_exist = True

		if config_is_exist == True:
			self.button_config.visible = "1"



	if "formbutton_update_plugin" in request.arguments:
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
				plugin.delete()

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

	if "op" in request.arguments and request.arguments.get("op") == "export":
		plugin_id = request.arguments.get("plugin_id", "")
		plugin = Plugins.get_by_id(int(plugin_id))
		output = plugin.export()
		output_len = output.tell()
		output.seek(0)
		response.send_file(plugin.name.encode("utf8") + ".xml", output_len, output)

	if "op" in request.arguments and request.arguments.get("op") == "export_db":
		db_name = request.arguments.get("db", "")
		plugin = Plugins.get_by_id(int(request.arguments.get("plugin_id", 0)))
		if plugin:
			output = DatabaseManager(plugin.guid).export_db(db_name)
			from StringIO import StringIO
			outp = StringIO()
			outp.write( output.read() )
			outp_len = outp.tell()
			outp.seek(0)
			response.send_file(db_name, outp_len, outp)


	if "formbutton_apply" in request.arguments:
		#raise Exception("1")
		macros_id = request.arguments.get("formtext_macro_id", "")
		macros = Macros.get_by_id(macros_id)
		if "uploader" in request.arguments:
			picture = request.arguments.get("uploader", "", castto=Attachment)
			picture_name = ""
			if picture:
				macros.macros_picture = picture_name = str(uuid4())
				application.storage.write(picture_name, picture.handler.read())
		macros.save()

		plugin_id = request.arguments.get("id", "")
		plugin = Plugins.get_by_id(int(plugin_id))
		macros = plugin.get_macros()

		widget_macros = WidgetMacros()
		widget_macros.set_data(macros)
		widget_macros.render(self.datatable_macros)


	if "formbutton_apply_db" in request.arguments:
		db_file = request.arguments.get("uploader_db", "", castto=Attachment)
		if db_file:
			db_name = request.arguments.get("formtext_db_name") if request.arguments.get("formtext_db_name") else db_file.name
			if db_name in DatabaseManager(plugin.guid).databaselist:
				#db_name = "new_" + db_name
				self.growl.title = lang["error"]
				self.growl.text	= "DB '"+db_name+"' exist"
				self.growl.visible = "1"
			else:
				if plugin:
					DatabaseManager(plugin.guid).import_db(db_name, db_file.handler)
			widget_db = WidgetPluginDB()
			widget_db.set_data(DatabaseManager(plugin.guid).databaselist)
			widget_db.render(self.datatable_db)

	if "formbutton_update_db" in request.arguments:
		db_file = request.arguments.get("uploader_db", "", castto=Attachment)
		if db_file:
			db_name = request.arguments.get("formtext_db_name") if request.arguments.get("formtext_db_name") else db_file.name
			if plugin:
				old_db_name = request.arguments.get("formtext_old_db_name", "")
				try:
					DatabaseManager(plugin.guid).delete_db(old_db_name)
				except:
					pass
			DatabaseManager(plugin.guid).import_db(db_name, db_file.handler)
			widget_db = WidgetPluginDB()
			widget_db.set_data(DatabaseManager(plugin.guid).databaselist)
			widget_db.render(self.datatable_db)

	if "formbutton_apply_resource" in request.arguments:
		resource_file = request.arguments.get("uploader_resource", "", castto=Attachment)
		resource_name = resource_file.name
		if resource_file:
			if resource_name in ResourceFolderManager(plugin.guid).resourcelist:
				#resource_name = "new_" + resource_name
				self.growl.title = lang["error"]
				self.growl.text	= "Resource '"+resource_name+"' exist"
				self.growl.visible = "1"
			else:
				if plugin:
					ResourceFolderManager(plugin.guid).import_res(resource_name, resource_file.handler)

		widget_resource = WidgetResource()
		widget_resource.set_data(ResourceFolderManager(plugin.guid).resourcelist, plugin.guid)
		widget_resource.render(self.datatable_resource)


main()
