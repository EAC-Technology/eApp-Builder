import localization

lang = localization.get_lang()

self.dialog_proadmin.show = "1"
self.dialog_proadmin.title = lang["proadmin_connection"]
self.dialog_proadmin.hpt.htmlcode = lang["proadmin_text"]

text = {
	"close_btn"				: [ self.dialog_proadmin.button_close ],
}
for k, v in text.items():
	for element in v:
		if 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]