from class_macros_events import MacrosEvents
import json
import localization


lang = localization.get_lang()
if "Value" in request.arguments:
	if request.arguments.get("Value") == "0":
		self.form_macros.text_event.visible = "1"
		self.form_macros.formlist_event_list.visible = "1"
		events = MacrosEvents.get_events()
		self.form_macros.formlist_event_list.value = json.dumps({event.id : event.name for event in events})

		self.form_macros.text_picture.visible = "0"
		self.form_macros.formcheckbox_on_board.visible = "0"
		self.form_macros.uploader.visible = "0"
		self.form_macros.hypertext_img.visible = "0"
	else:
		self.form_macros.text_event.visible = "0"
		self.form_macros.formlist_event_list.visible = "0"

		self.form_macros.formcheckbox_on_board.visible = "1"

		self.form_macros.hypertext_img.visible = "1"

self.form_macros.text_event.value = lang["edit_macros_event_title"]
self.form_macros.formcheckbox_on_board.label = lang["edit_macros_on_board_checkbox"]
