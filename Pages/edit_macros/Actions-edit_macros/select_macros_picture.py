from class_macros import Macros
import localization


lang = localization.get_lang()
if "Value" in request.arguments:
	if request.arguments.get("Value") == "0":
		self.form_macros.text_picture.visible = "0"
		self.form_macros.uploader.visible = "0"
		self.form_macros.hypertext_img.visible = "0"
	else:
		self.form_macros.text_picture.visible = "1"
		self.form_macros.uploader.visible = "1"

		self.form_macros.hypertext_img.visible = "1"
		if "macros_id" in session:
			macros = Macros.get_by_id(session.get("macros_id"))
			self.form_macros.hypertext_img.htmlcode = "<img src='/get_image?id=%s'/>"%macros.macros_picture if macros.macros_picture else ""

self.form_macros.text_picture.value = lang["edit_macros_picture_title"]
