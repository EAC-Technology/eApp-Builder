from api_helper import *
from models import Widget


#@license_confirmed
@authenticated
@error_handler
@parse_json
def main( data ):

	action = data.get("action", "read")
	input_data = data.get("data", {})
	result = {}

	if action == "create":
		widget = Widget()
		widget.fill_from_json(input_data)
		widget.save(b64source=input_data.get("b64source", None))
		result[widget.guid] = widget.to_json()

	elif action == "read":
		for wid_guid in input_data:
			widget = Widget.get(guid=wid_guid)
			result[wid_guid] = widget.to_json(include=["b64source"]) if widget else None

	elif action == "update":
		for widget_guid in input_data:
			widget = Widget.get(guid=widget_guid)
			wid_json = input_data[widget_guid]
			if widget:
				widget.fill_from_json(wid_json)
				widget.save(b64source=input_data.get("b64source", None))
				result[widget_guid] = widget.to_json(include=["b64source"])

	elif action == "delete":
		for widget_guid in input_data:
			widget = Widget.get(guid=widget_guid)
			if widget:
				widget.delete()
				result[widget_guid] = "deleted"
			else:
				result[widget_guid] = "not_found"

	write_response( result )

main()
