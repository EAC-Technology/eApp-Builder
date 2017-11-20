import json

keys = request.arguments[ "keyList" ]
widget = session.get("addUserGroupWidget",None)
if keys and widget:
	widget.add_subject(json.loads(keys))
