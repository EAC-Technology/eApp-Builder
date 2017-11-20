from api_helper import *
from models import Resource


#@license_confirmed
@authenticated
@error_handler
@parse_json
def main( data ):

	action = data.get("action", "read")
	input_data = data.get("data", {})
	result = {}

	if action == "create":
		resource = Resource()
		resource.fill_from_json(input_data)
		resource.save(b64content=input_data.get("b64content", None))
		result[resource.guid] = resource.to_json()

	elif action == "read":
		for res_guid in input_data:
			resource = Resource.get(guid=res_guid)
			result[res_guid] = resource.to_json(include=["b64content"]) if resource else None

	elif action == "update":
		for resource_guid in input_data:
			resource = Resource.get(guid=resource_guid)
			res_json = input_data[resource_guid]
			if resource:
				resource.fill_from_json(res_json)
				resource.save(b64content=res_json.get("b64content", None))
				result[resource_guid] = resource.to_json(include=["b64content"])


	elif action == "delete":
		for resource_guid in input_data:
			resource = Resource.get(guid=resource_guid)
			if resource:
				resource.delete()
				result[resource_guid] = "deleted"
			else:
				result[resource_guid] = "not_found"

	write_response( result )

main()
