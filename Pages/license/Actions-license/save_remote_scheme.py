import ProAdmin
import localization
lang = localization.get_lang()

from class_remote_settings import RemoteSettings

login 		= request.arguments["formtext_login"]
password 	= request.arguments["formpassword"]
server 		= request.arguments["formtext_server"]

try:
	from vdom_remote_api import VDOMService
	from md5 import md5

#	connect = VDOMService.connect(server, login, md5( password ).hexdigest(),
#					"491d4c93-4089-4517-93d3-82326298da44")

	connect = VDOMService(server, login, md5( password ).hexdigest(),
					"491d4c93-4089-4517-93d3-82326298da44").open_session()

	RemoteSettings(login, password, server).save()

	#ProAdmin.scheme().delete()
	ProAdmin.unregister_default_scheme()
	ProAdmin.scheme()
	ProAdmin.logoff()

	from class_license import License
	License().confirmed = "True"

	self.action("goTo",["/logoff"])

except Exception,ex:
	error = str(ex.__class__).replace("<","&lt")
	err_txt = ""
	if "socket.gaierror" in error :
		err_txt = lang["socket.gaierror"]
	elif "socket.error" in error:
		err_txt = lang["socket.error"]
	elif "faultType" in error or "NameError" in error:
		err_txt = lang["faultType"]
	else:
		err_txt = error

	self.growl.action("show",[lang["error"],err_txt])