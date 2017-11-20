import ProAdmin
from class_remote_settings import RemoteSettings
from vdom_remote_api import VDOMService
from md5 import md5
import localization

lang = localization.get_lang()

try:

	host 		= request.shared_variables["host"]
	login 		= request.shared_variables["login"]
	password 	= request.shared_variables["password"]
	app_id		= '491d4c93-4089-4517-93d3-82326298da44'

	try:
		RemoteSettings(login, password, host).save()
		ProAdmin.logoff()
		ProAdmin.unregister_default_scheme()
		ProAdmin.scheme()
		self.action("goTo",["/proadmin_management"])

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
			raise
			err_txt = error

		self.growl.action("show",["Error",err_txt])

except Exception, ex:
	self.growl.action( 'show', [ lang["error_title"], str(ex) ] )