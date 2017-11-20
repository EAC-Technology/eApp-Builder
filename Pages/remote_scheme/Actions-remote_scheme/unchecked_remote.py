import localization
lang = localization.get_lang()

self.container_remote.form_remote.formradiogroup_remote.formradiobutton_remote.state = "0"

text = {
		"proadmin_connection"			: [ self.container_remote.form_remote.formradiogroup_remote.formradiobutton_remote, self.container_remote_state.text_current_scheme ],
}
for k, v in text.items():
	for element in v:
		if 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]