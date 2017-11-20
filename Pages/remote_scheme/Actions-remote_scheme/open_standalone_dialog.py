import localization

lang = localization.get_lang()

self.dialog_standalone.show = "1"
self.dialog_standalone.title = lang["standalone"]
self.dialog_standalone.hpt.htmlcode = lang["standalone_text"]

text = {
	"close_btn"				: [ self.dialog_standalone.button_close ],
}
for k, v in text.items():
	for element in v:
		if 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]