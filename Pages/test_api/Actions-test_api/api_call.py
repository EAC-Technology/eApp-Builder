import managers
import json

args = request.arguments

appid = application.id
container = "5073ff75-da99-44fb-a5d7-e44e5ab28598"
action = args.get("api_name")
xml_param = ""
xml_data = args["api_data"]

#raise Exception(xml_data)

# auto login
ret = managers.dispatcher.dispatch_action(appid, container, "login", xml_param,
	'{"login": "root", "password": "root"}'
)

ret = managers.dispatcher.dispatch_action(appid, container, action, xml_param, xml_data)
if isinstance(ret, unicode):
	ret = ret.encode("utf8","ignore")

ret = ret.replace("\\n\\n", "<br/>")

ret = json.loads(ret)
#raise Exception(ret)
self.hypertext1.htmlcode = "<pre>"+json.dumps(ret, indent=2)+"</pre>"
