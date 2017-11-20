import managers
import json

from models import *
from unittests_resource import TestResourceApi


args = request.arguments

appid = application.id
container = "5073ff75-da99-44fb-a5d7-e44e5ab28598"
#action = args.get("api_name")
xml_param = ""
#xml_data = args["api_data"]

# auto login
def login():
	return managers.dispatcher.dispatch_action(appid, container, "login", xml_param,
		'{"login": "root", "password": "root"}'
	)

def apicall(action, xml_data):
	return managers.dispatcher.dispatch_action(appid, container, action, "", xml_data)

def res_test():
	w = Workspace(name="Res test workspace")
	w.save()
	logs = []

	try:
		a = Application(name="Res test app", workspace_id=w.guid)
		a.save()

		w_objects = json.loads(apicall("get_objects", "{}"))[1]
		w_search = [ws for ws in w_objects["workspaces"] if ws["guid"] == w.guid][0]
		logs.append("<b>{}</b> workspace created ".format(w_search["name"]))

		ret = apicall("eapp_resources", {})[1]


	finally:
		w.delete()

	return logs

test_case = args.get("formlist1", "res_test")

result = ""
login()

if test_case == "res_test":
	result = res_test()
elif test_case == "res_unittest":
	TestResourceApi.main()



#	ret = managers.dispatcher.dispatch_action(appid, container, action, xml_param, xml_data)
#if isinstance(ret, unicode):
#	ret = ret.encode("utf8","ignore")

self.hypertext1.htmlcode = json.dumps(result, indent=4)
