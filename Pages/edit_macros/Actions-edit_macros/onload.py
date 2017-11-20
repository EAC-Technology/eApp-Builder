from class_macros import Macros
from class_macros_events import MacrosEvents
from vscript import errors, generic, boolean, string, v_empty, v_true_value, v_false_value, as_string, engine
import json
import VEE_events

from class_acl_user import ACLUser
import localization
from class_license import License
import base64
from utils.uuid import uuid4
import cgi
from widget_localization import LocalizationWidget
import localization


lang = localization.get_lang()
if not License().confirmed:
	response.redirect("/license.vdom")

try:

	user = ACLUser.current()

	if not user or not user.is_admin():
		response.redirect("/contact.vdom")

	events = MacrosEvents.get_events()
	self.form_macros.formlist_event_list.value = json.dumps({event.id : event.name for event in events})

	macros_id = session.get("macros_id")
	#self.form_macros.formbutton_delete.visible = "0"

	if macros_id:
		macros = Macros.get_by_id(macros_id)
		if macros.class_name:
			self.form_macros.formcheckbox_is_button.state = "0"
			self.form_macros.text_picture.visible = "0"
			self.form_macros.formcheckbox_on_board.visible = "0"
			self.form_macros.uploader.visible = "0"

			self.form_macros.formlist_event_list.visible = "1"
			self.form_macros.text_event.visible = "1"

			event = MacrosEvents.get_by_name(macros.class_name)
			self.form_macros.formlist_event_list.selectedvalue = event.id
		else:
			self.form_macros.formcheckbox_is_button.state = "1"
			self.form_macros.formcheckbox_on_board.visible = "1"
			self.form_macros.formlist_event_list.visible = "0"
			self.form_macros.text_event.visible = "0"

		if macros.on_board == "1":
			self.form_macros.formcheckbox_on_board.state = "1"
			self.form_macros.text_picture.visible = "1"
			self.form_macros.uploader.visible = "1"


		self.form_macros.formbutton_delete.visible = "1"
		self.form_macros.codeeditor_macros_body.value = macros.code
		self.form_macros.formtext_name.value = macros.name
		self.form_macros.hypertext_img.htmlcode = "<img src='/get_image?id=%s'/>"%macros.macros_picture if macros.macros_picture else ""



	if "formbutton_apply" in request.arguments:

		source = self.form_macros.codeeditor_macros_body.value = request.arguments.get("codeeditor_macros_body", "")
		name = self.form_macros.formtext_name.value = request.arguments.get("formtext_name", "")
		event = self.form_macros.formlist_event_list.selectedvalue = request.arguments.get("formlist_event_list")
		is_button = self.form_macros.formcheckbox_is_button.state = request.arguments.get("formcheckbox_is_button", "0")
		on_board = self.form_macros.formcheckbox_is_button.state = request.arguments.get("formcheckbox_on_board", "0")
		picture = request.arguments.get("uploader", "", castto=Attachment)
		picture_name = ""
		if picture:
			picture_name = str(uuid4())
			application.storage.write(picture_name, picture.handler.read())
		elif macros_id:
			macros_object = Macros.get_by_id(macros_id)
			picture_name = macros_object.macros_picture
			self.form_macros.hypertext_img.htmlcode = "<img src='/get_image?id=%s'/>"%picture_name if picture_name else ""
		#raise Exception(event)
		class_name = ""
		if not source or not name:
			self.growl.title = lang["error"]
			self.growl.text = lang["fill_all_fields_error"]
			self.growl.visible = "1"
		else:
			if is_button == "0":
				for e in events:
					if e.id == int(event):
						class_name = e.name

			macros = Macros()
			macros.id 			= macros_id if macros_id else None
			macros.name 		= name
			macros.code 		= source
			macros.class_name	= class_name
			macros.is_button_macros = is_button
			macros.on_board = on_board
			macros.macros_picture = picture_name
			macros.save()
			del session["macros_id"]
			response.redirect("/macros_settings.vdom")

	elif "formbutton_check" in request.arguments:
		if macros_id:
			macros = Macros.get_by_id(macros_id)

			source = self.form_macros.codeeditor_macros_body.value = request.arguments.get("codeeditor_macros_body", "")
			self.form_macros.formtext_name.value = request.arguments.get("formtext_name", "")
			self.form_macros.formlist_event_list.selectedvalue = request.arguments.get("formlist_event_list")
			self.form_macros.formcheckbox_is_button.state = request.arguments.get("formcheckbox_is_button", "0")
			self.form_macros.formcheckbox_is_button.state = request.arguments.get("formcheckbox_on_board", "0")
			self.form_macros.hypertext_img.htmlcode = "<img src='/get_image?id=%s'/>"%macros.macros_picture if macros.macros_picture else ""

			if source:
				cmpl = engine.vcompile(source)
				if not cmpl[1]:
					self.growl.title = lang["error"]
					self.growl.text = lang["vscript_not_compiled_error"]
					self.growl.visible = "1"
			else:
				self.growl.title = lang["error"]
				self.growl.text = lang["type_macros_code_error"]
				self.growl.visible = "1"

		else:
			self.growl.title = lang["error"]
			self.growl.text = lang["fill_macros_fields_error"]
			self.growl.visible = "1"


	elif "formbutton_export" in request.arguments:
		macros = Macros.get_by_id(macros_id)

		self.form_macros.codeeditor_macros_body.value = request.arguments.get("codeeditor_macros_body", "")
		self.form_macros.formtext_name.value = request.arguments.get("formtext_name", "")
		self.form_macros.formlist_event_list.selectedvalue = request.arguments.get("formlist_event_list")
		self.form_macros.formcheckbox_is_button.state = request.arguments.get("formcheckbox_is_button", "0")
		self.form_macros.formcheckbox_is_button.state = request.arguments.get("formcheckbox_on_board", "0")
		self.form_macros.hypertext_img.htmlcode = "<img src='/get_image?id=%s'/>"%macros.macros_picture if macros.macros_picture else ""

		if type(macros_id) != list:
			macros_id = [ macros_id ]

		output = Macros.export(macros_id)
		output_len = output.tell()
		output.seek(0)
		response.send_file(request.arguments.get("formtext_name", "") + ".xml", output_len, output)

	elif "formbutton_cancel" in request.arguments:
		del session["macros_id"]
		response.redirect("/macros_settings.vdom")

except Exception, ex:
	self.growl.title = lang["error"]
	self.growl.text = lang["unknown_error"]
	self.growl.active = "1"

localization_wdgt = LocalizationWidget()

localization_wdgt.add_controls( "edit_macros_page_title", self )
localization_wdgt.add_controls( "edit_macros_area_caption", self.page_title )
localization_wdgt.add_controls( "edit_macros_check_btn", self.form_macros.formbutton_check )
localization_wdgt.add_controls( "edit_macros_export_btn", self.form_macros.formbutton_export )
localization_wdgt.add_controls( "dialog_apply_btn", self.form_macros.formbutton_apply )
localization_wdgt.add_controls( "dialog_cancel_btn", self.form_macros.formbutton_cancel )
localization_wdgt.add_controls( "dialog_delete_btn", self.form_macros.formbutton_delete )
localization_wdgt.add_controls( "edit_macros_body_title", self.form_macros.text_body )
localization_wdgt.add_controls( "edit_macros_event_title", self.form_macros.text_event )
localization_wdgt.add_controls( "edit_macros_name_title", self.form_macros.text_macros_name )
localization_wdgt.add_controls( "edit_macros_button_macros_checkbox", self.form_macros.formcheckbox_is_button )
localization_wdgt.add_controls( "edit_macros_picture_title", self.form_macros.text_picture )
localization_wdgt.add_controls( "edit_macros_on_board_checkbox", self.form_macros.formcheckbox_on_board )


localization_wdgt.render()
