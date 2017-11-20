from widget_user_group_dialog import authenticated, error_handler, administrator, license_confirmed

@license_confirmed
@authenticated
@administrator
@error_handler
def main():

	from class_macro import Macros
	from class_plugins import Plugins
	import cgi, localization


	lang = localization.get_lang()

	macros_id = request.arguments.get("id")
	response.shared_variables["macro_id"] = macros_id
	plugin = ""
	if macros_id:
		macros = Macros.get_by_id(macros_id)
		plugin = Plugins.get_by_guid(macros.plugin_guid)
		if plugin.protected:
				response.redirect("/plugins.vdom")
		self.form_macros.codeeditor_macros_body.value = macros.code if macros.code else ""


	if "formbutton_apply" in request.arguments:
		if plugin:
			source = self.form_macros.codeeditor_macros_body.value = request.arguments.get("codeeditor_macros_body", "")
			macros = Macros.get_by_id(macros_id) if macros_id else Macros()
			macros.code 		= source
			macros.save()
			response.redirect("/plugin_details?id=" + str(plugin.id))
		else:
			self.growl.title = lang["error"]
			self.growl.text = "Unknown macro"
			self.growl.visible = "1"

	elif "formbutton_check" in request.arguments:
		if macros_id:
			source = self.form_macros.codeeditor_macros_body.value = request.arguments.get("codeeditor_macros_body", "")
			if source:

				from VEE_tools import compile, VScriptComlipationError, PythonCompilationError
				try:
					compile( source )
				except VScriptComlipationError as error:
					self.growl.title = lang["error"]
					self.growl.text = u"VScript Compilation Error (Line {line}): {msg}".format(
									line = error.line,
									msg	 = error.message )
					self.growl.visible = "1"

				except PythonCompilationError as error:
					self.growl.title = lang["error"]
					self.growl.text = u"Python Compilation Error: {msg}".format(
									msg	 = error.message )
					self.growl.visible = "1"

			else:
				self.growl.title = lang["error"]
				self.growl.text = lang["type_macros_code_error"]
				self.growl.visible = "1"

		else:
			self.growl.title = lang["error"]
			self.growl.text = lang["fill_macros_fields_error"]
			self.growl.visible = "1"

	elif "formbutton_cancel" in request.arguments:
		response.redirect("/plugin_details?id=" + str(plugin.id)) if plugin else response.redirect("/plugins")


main()
