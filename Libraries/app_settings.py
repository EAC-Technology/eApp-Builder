"""
	Settings file. Need to define a way to automatically select which settings class to use
"""

class settings_common:

	TEST_MODE = False
	SOFT_DELETE = False
	DEVELOP_AUTOLOGIN = False  # no need to login to have access to certain pages

	DEV_LOGIN = 'root'
	DEV_PASSWORD = 'root'


class settings_dev(settings_common):

	TEST_MODE = True
	SOFT_DELETE = False
	DEVELOP_AUTOLOGIN = True

	DEV_LOGIN = 'root'
	DEV_PASSWORD = 'root'

#from cgi import escape
#raise Exception(', '.join([escape("%s=%s" % (key, getattr(request, key))) for key in dir(request)]))

dev_hosts = [
	"eapp-sib.vdombox.ru",  # sibirsky machine
]
current_host = request.headers.get('host')
settings = settings_common

if current_host in dev_hosts:
	settings = settings_dev
