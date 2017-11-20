import localization
lang = localization.get_lang()

self.container_local.form_local.formradiogroup_local.formradiobutton_local.state = "0"


text = {
	"standalone"					: [ self.container_local.form_local.formradiogroup_local.formradiobutton_local, self.container_local_state.text_current_scheme ],
}
for k, v in text.items():
	for element in v:
		if 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]