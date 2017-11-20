from vdom_trace import Trace

try:
	import ProAdmin
	import json
	from class_remote_settings import RemoteSettings
	import managers

	params = request.arguments.get( 'xml_data' )
	params = json.loads( params )

	server  =  params["server"] if "server" in params else ""
	login  =  params["login"] if "login" in params else ""
	password  =  params["password"] if "password" in params else ""

	if managers.request_manager.current.session().user == "root":
		if server:
			RemoteSettings(login, password, server).save()
			ProAdmin.unregister_default_scheme()
		else:
			if RemoteSettings.get_remote_setting():
				RemoteSettings.delete()
				ProAdmin.unregister_default_scheme()
	else:
		raise Exception("You can't change scheme")

	session[ 'response' ] = json.dumps( ["success"] ) #added [] 10.01.2013 Nikita

except:
	session[ 'response' ] = json.dumps( [ 'error', Trace.exception_trace() ] )
