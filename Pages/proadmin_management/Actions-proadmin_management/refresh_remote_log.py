from vdom_remote_api import VDOMService,VDOMServiceSingleThread
from socket import gethostbyname
import ProAdmin
from md5 import md5
from proadmin_remote_sync import RemoteSyncClient
from class_remote_settings import RemoteSettings
import localization
from SOAPpy.Errors import Error, HTTPError
from SOAPpy.Types import faultType
lang = localization.get_lang()

try:
	remote = RemoteSettings.get_remote_setting()

	host 		= remote.server
	login 		= remote.login
	password 	= remote.password
	app_id		= '491d4c93-4089-4517-93d3-82326298da44'

	host_to_check = host.replace("https://", "").replace("http://", "")
	correct_flag = True
	connection_to_ip = open_session = proadmin_version = ""

	try:
		connection_to_ip = "<p class='success'><span>" + lang["connect_ip_success"] + gethostbyname(host_to_check) + "</span></p>"
	except:
		correct_flag = False
		connection_to_ip = "<p class='failed'><span>" + lang["connect_ip_fail"] + "</span></p>"
	if correct_flag:
		try:
			if isinstance(VDOMService( host, login, md5( password ).hexdigest(), app_id ).open_session(), VDOMServiceSingleThread):
				open_session = "<p class='success'><span>" + lang["open_session_success"] + "(" + host + ", " + login + ")</span></p>"
			else:
				correct_flag = False
				open_session = "<p class='failed'><span>" + lang["open_session_fail"] + "</span></p>"
		except Error, ex:
			correct_flag = False
			error_text = ""
			if isinstance(ex, faultType):
				error_text = lang["incorrect_login"]
			elif isinstance(ex, HTTPError):
				error_text = lang["no_vdom"]
			open_session = "<p class='failed'><span>" + error_text + "</span></p>"
		if correct_flag:
			try:
				version = RemoteSyncClient( VDOMService( host, login, md5( password ).hexdigest(), app_id ) ).proadmin_version()
				if version:
					proadmin_version = "<p class='success'><span>ProAdmin (" + version + ")</span></p>"
				else:
					correct_flag = False
					proadmin_version = "<p class='failed'><span>" + lang["proadmin_connection_fail"] + "</span></p>"
			except:
				correct_flag = False
				proadmin_version = "<p class='failed'><span>" + lang["proadmin_connection_fail"] + "</span></p>"
	host_name = login + lang["at"] + host
	host_name_to_show = host_name[:30] + "..." if len(host_name) > 30 else host_name
	self.container_remote_state.hpt_host.htmlcode = "<span style='font-size:11pt; font-weight:bold;' title='" + host_name + "'>" + host_name_to_show + "</span>"
	self.container_remote_state.hpt_conn.htmlcode = connection_to_ip + open_session + proadmin_version
	self.container_remote_state.image_current.value = "79597b3d-3d05-4462-bc50-02fc85c11da3" if correct_flag else "5c4aba86-109b-4e17-9170-528336f364d2"

	if ProAdmin.scheme().is_remote():
		self.container_remote_state.container_proadmin.text_last_sync.value = lang["last_sync_text"] + ( str(ProAdmin.scheme().sync_datetime.strftime("%H:%M:%S %d.%m.%Y")) if ProAdmin.scheme().sync_datetime else "?" )
		self.container_remote_state.container_proadmin.text_sync_status.value = lang["syns_state_text"] + "OK" if ProAdmin.scheme().is_sync_active() else lang["syns_state_text"] + "FAIL"
		self.container_remote_state.container_proadmin.text_objects.value = lang["object_text"] + str(len( ProAdmin.application().child_objects( recursive=True ) ))
		self.container_remote_state.container_proadmin.text_users.value = lang["user_text"] + str(len( ProAdmin.application().get_users() ))
except Exception, ex:
	self.growl.action( 'show', [ lang["error_title"], str(ex) ] )
