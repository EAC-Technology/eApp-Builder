name = request.arguments[ "Name" ]
widget = session.get("addUserGroupWidget",None)
if name and widget:
	if name == "container_group":
		widget.tab_changed(1, self.form_search.some_text)
	elif name == "container_user":
		widget.tab_changed(0, self.form_search.some_text)
