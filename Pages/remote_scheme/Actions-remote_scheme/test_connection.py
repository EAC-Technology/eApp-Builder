from vdom_remote_api import VDOMService, VDOMServiceSingleThread
from socket import gethostbyname
import ProAdmin
from md5 import md5
from proadmin_remote_sync import RemoteSyncClient
import localization
from SOAPpy.Errors import Error, HTTPError
from SOAPpy.Types import faultType

lang = localization.get_lang()

host 		= request.shared_variables["host"]
login 		= request.shared_variables["login"]
password 	= request.shared_variables["password"]
app_id		= '491d4c93-4089-4517-93d3-82326298da44'

correct_flag = True
connection_to_ip = open_session = proadmin_version = ""

if not host or not login or not password:
	self.growl.action("show", [lang["error_title"], lang["fill_all_fields_error"]])
	self.container_remote.form_remote.bar_test_res.visible = "0"
	self.container_remote.form_remote.hpt_conn.visible = "0"
	self.container_remote.form_remote.hpt_conn.height = "18"
	self.container_remote.height = self.container_remote.form_remote.height = "285"
	self.container_remote.form_remote.formbutton_test_sso.top = self.container_remote.form_remote.formbutton_apply.top = self.container_remote.form_remote.container_disabled.top = self.container_remote.form_remote.formbutton_reset.top = self.container_remote.form_remote.formbutton_test.top = "228"
	self.container_remote.form_remote.container_disabled.visible = "1"
	self.container_remote.form_remote.formbutton_reset.visible = "1"
else:
	host_to_check = host.replace("https://", "").replace("http://", "")
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
				proadmin_info = RemoteSyncClient( VDOMService( host, login, md5( password ).hexdigest(), app_id ) ).proadmin_version(True)

				# fix for old version of ProAdmin
				if not isinstance( proadmin_info, dict ):
					proadmin_info = {
						'name'		: 'ProAdmin',
						'version'	: proadmin_info,
					}

				if proadmin_info:
					proadmin_version = "<p class='success'><span>" + proadmin_info["name"] + " (" + proadmin_info["version"] + ")</span></p>"
				else:
					correct_flag = False
					proadmin_version = "<p class='failed'><span>" + lang["proadmin_connection_fail"] + "</span></p>"
			except:
				correct_flag = False
				proadmin_version = "<p class='failed'><span>" + lang["proadmin_connection_fail"] + "</span></p>"

	self.container_remote.form_remote.hpt_conn.htmlcode = connection_to_ip + open_session + proadmin_version

	self.container_remote.form_remote.bar_test_res.visible = "1"
	self.container_remote.form_remote.hpt_conn.visible = "1"
	self.container_remote.form_remote.hpt_conn.height = "110"
	self.container_remote.height = self.container_remote.form_remote.height = "385"
	self.container_remote.form_remote.container_disable.height = str(int(self.container_remote.height) - 60)
	self.container_remote.form_remote.formbutton_test_sso.top = self.container_remote.form_remote.formbutton_apply.top = self.container_remote.form_remote.container_disabled.top = self.container_remote.form_remote.formbutton_reset.top = self.container_remote.form_remote.formbutton_test.top = "328"
	self.container_remote.form_remote.container_disabled.visible = "0" if correct_flag else "1"
	self.container_remote.form_remote.formbutton_reset.visible = "1"

self.container_remote.form_remote.formradiogroup_remote.formradiobutton_remote.state = "1"
self.container_remote.form_remote.container_disable.visible = "0"
self.container_remote.form_remote.formtext_host.value = host if host else ""
self.container_remote.form_remote.formtext_login.value = login if login else ""
self.container_remote.form_remote.formpassword.value = '*'*len(password) if password else ""


text = {
	"settings_remote_page_title"	: [ self.text_page_title ],
	"text_current_scheme"			: [ self.text_current_scheme ],
	"standalone"					: [ self.container_local.form_local.formradiogroup_local.formradiobutton_local, self.container_local_state.text_current_scheme ],
	"proadmin_connection"			: [ self.container_remote.form_remote.formradiogroup_remote.formradiobutton_remote, self.container_remote_state.text_current_scheme ],
	"login"							: [ self.container_remote.form_remote.text_login ],
	"password"						: [ self.container_remote.form_remote.text_password ],
	"host"							: [ self.container_remote.form_remote.text_host ],
	"test_btn"						: [ self.container_remote.form_remote.formbutton_test ],
	"use_settings_btn"				: [ self.container_remote.form_remote.formbutton_apply,self.container_local.form_local.formbutton_apply ],
	"refresh_btn"					: [ self.container_remote_state.button_refresh ],
	"test_sso_btn"					: [ self.container_remote.form_remote.formbutton_test_sso ],
	"reset_btn"						: [ self.container_remote.form_remote.formbutton_reset ],
}
for k, v in text.items():
	for element in v:
		if 'text' in dir( element ):
			element.text = lang[k]
		elif 'label' in dir( element ):
			element.label = lang[k]
		elif 'value' in dir( element ):
			element.value = lang[k]
