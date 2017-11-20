from class_remote_settings import RemoteSettings
import localization
from vdom_remote_api import VDOMService,VDOMServiceSingleThread
from socket import gethostbyname
import ProAdmin
from md5 import md5
from proadmin_remote_sync import RemoteSyncClient
from proadmin_sso import SSOClient
from proadmin_utils import Utils
from SOAPpy.Errors import Error, HTTPError
from SOAPpy.Types import faultType

lang = localization.get_lang()

app_id	= ProAdmin.PROADMIN_APPLICATION_GUID

try:
	if not Utils.is_admin():
		response.redirect("/proadmin.vdom")

	# TEST SSO CODE =================================================
	ssoclient = SSOClient( request, response )
	if ssoclient.test_sso( check = True ) and session.get("sso_tested", "0") == "1":
		session["sso_tested"] = "0"
		self.dialog_sso_success.show = "1"
	# TEST SSO CODE =================================================

	remote = RemoteSettings.get_remote_setting()

	if remote:
		host_to_check = remote.server.replace("https://", "").replace("http://", "")

		self.container_remote.form_remote.formradiogroup_remote.formradiobutton_remote.state = "1"
		self.container_remote.form_remote.container_disable.visible = "0"
		self.container_remote.form_remote.formtext_host.value = response.shared_variables["host"] = remote.server
		self.container_remote.form_remote.formtext_login.value = response.shared_variables["login"] = remote.login
		self.container_remote.form_remote.formpassword.value = "*" * len(remote.password)
		response.shared_variables["password"] = remote.password
		self.container_remote_state.visible = "1"

		correct_flag = True
		try:
			connection_to_ip = "<p class='success'><span>" + lang["connect_ip_success"] + gethostbyname(host_to_check) + "</span></p>"
			import os
			command = os.system('ping -c 1 ' + gethostbyname(host_to_check))
			if command != 0: raise
		except:
			correct_flag = False
			connection_to_ip = "<p class='failed'><span>" + lang["connect_ip_fail"] + "</span></p>"

		if correct_flag:
			try:
				if isinstance(VDOMService( remote.server, remote.login, md5( remote.password ).hexdigest(), app_id ).open_session(), VDOMServiceSingleThread):
					open_session = "<p class='success'><span>" + lang["open_session_success"] + "(" + remote.server + ", " + remote.login + ")</span></p>"
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
					proadmin_info = RemoteSyncClient( VDOMService( remote.server, remote.login, md5( remote.password ).hexdigest(), app_id ) ).proadmin_version(True)
					if proadmin_info:
						proadmin_version = "<p class='success'><span>" + proadmin_info["name"] + " (" + proadmin_info["version"] + ")</span></p>"
					else:
						correct_flag = False
						proadmin_version = "<p class='failed'><span>" + lang["proadmin_connection_fail"] + "</span></p>"
				except:
					correct_flag = False
					proadmin_version = "<p class='failed'><span>" + lang["proadmin_connection_fail"] + "</span></p>"

		host_name = remote.login + lang["at"] + remote.server
		host_name_to_show = host_name[:30] + "..." if len(host_name) > 30 else host_name
		self.container_remote_state.hpt_host.htmlcode = "<span style='font-size:11pt; font-weight:bold;' title='" + host_name + "'>" + host_name_to_show + "</span>"
		self.container_remote_state.hpt_conn.htmlcode = connection_to_ip + open_session + proadmin_version
		self.container_remote_state.image_current.value = "79597b3d-3d05-4462-bc50-02fc85c11da3" if correct_flag else "4ce4e4cb-8c9d-4099-a284-c413265fb3bb"

		if ProAdmin.scheme().is_remote():
			self.container_remote_state.container_proadmin.text_last_sync.value = lang["last_sync_text"] + ( str(ProAdmin.scheme().sync_datetime.strftime("%H:%M:%S %d.%m.%Y")) if ProAdmin.scheme().sync_datetime else "?" )
			self.container_remote_state.container_proadmin.text_sync_status.value = lang["syns_state_text"] + "OK" if ProAdmin.scheme().is_sync_active() else lang["syns_state_text"] + "FAIL"
			self.container_remote_state.container_proadmin.text_objects.value = lang["object_text"] + str(len( ProAdmin.application().child_objects( recursive=True ) ))
			self.container_remote_state.container_proadmin.text_users.value = lang["user_text"] + str(len( ProAdmin.application().get_users() ))
	else:
		self.container_local.form_local.formradiogroup_local.formradiobutton_local.state = "1"
		self.container_local_state.visible = "1"


except:
	pass



text = {
	"settings_remote_page_title"	: [ self.text_page_title ],
	"text_current_scheme"			: [ self.text_current_scheme ],
	"standalone"					: [ self.container_local.form_local.formradiogroup_local.formradiobutton_local, self.container_local_state.text_current_scheme ],
	"proadmin_connection"			: [ self.container_remote.form_remote.formradiogroup_remote.formradiobutton_remote, self.container_remote_state.text_current_scheme ],
	"login"							: [ self.container_remote.form_remote.text_login ],
	"password"						: [ self.container_remote.form_remote.text_password ],
	"host"							: [ self.container_remote.form_remote.text_host ],
	"apply_btn"						: [ self.dialog_test_sso.button_apply ],
	"test_btn"						: [ self.container_remote.form_remote.formbutton_test ],
	"use_settings_btn"				: [ self.container_remote.form_remote.formbutton_apply, self.container_local.form_local.formbutton_apply ],
	"refresh_btn"					: [ self.container_remote_state.button_refresh ],
	"test_sso_btn"					: [ self.container_remote_state.button_test_sso, self.container_remote.form_remote.formbutton_test_sso ],
	"close_btn"						: [ self.dialog_sso_success.button_close ],
	"cancel_btn"					: [ self.dialog_test_sso.button_cancel ],
	"warning_test_sso"				: [ self.dialog_test_sso.text_warning ],
	"success_sso"					: [ self.dialog_sso_success.text_success ],
	"restart_connectoin_btn"		: [ self.container_remote_state.button_restart ],
	"reset_btn"						: [ self.container_remote.form_remote.formbutton_reset ],
	"proadmin_management"			: [ self.page_title ]
}
for k, v in text.items():
	for element in v:
		if 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]
