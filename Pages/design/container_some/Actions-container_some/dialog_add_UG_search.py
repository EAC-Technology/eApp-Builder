text = request.arguments[ "searchfield" ]
widget = session.get("addUserGroupWidget",None)

if text and widget:
	widget.search(text)
	widget.search_render(self.cont.datatable)
