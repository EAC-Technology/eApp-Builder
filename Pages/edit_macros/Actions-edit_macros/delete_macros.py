from class_macros import Macros
import localization


lang = localization.get_lang()
macros_id = session.get("macros_id")

if macros_id:
	macros = Macros.get_by_id(macros_id)
	macros.delete()
	del session["macros_id"]
	self.action("goTo", ["/macros_settings.vdom"])
else:
	self.growl.action("show", [lang["error"], lang["macro_not_defined_error"]])
