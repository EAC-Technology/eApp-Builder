from class_remote_settings import RemoteSettings

remote = RemoteSettings.get_remote_setting()
if remote:
	self.container_remote.form_remote.formtext_host.value = response.shared_variables["host"] = remote.server
	self.container_remote.form_remote.formtext_login.value = response.shared_variables["login"] = remote.login
	self.container_remote.form_remote.formpassword.value = "*" * len(remote.password)
	response.shared_variables["password"] = remote.password
else:
	self.container_remote.form_remote.bar_test_res.visible = "1"
	self.container_remote.form_remote.hpt_conn.visible = "0"
	self.container_remote.form_remote.hpt_conn.height = "18"
	self.container_remote.height = self.container_remote.form_remote.height = "285"
	self.container_remote.form_remote.formbutton_test_sso.top = self.container_remote.form_remote.formbutton_apply.top = self.container_remote.form_remote.container_disabled.top = self.container_remote.form_remote.formbutton_reset.top = self.container_remote.form_remote.formbutton_test.top = "228"
	self.container_remote.form_remote.container_disabled.visible = "1"
	self.container_remote.form_remote.formbutton_reset.visible = "0"

	self.container_remote.form_remote.formradiogroup_remote.formradiobutton_remote.state = "0"
	self.container_remote.form_remote.container_disable.visible = "1"
	self.container_local.form_local.formradiogroup_local.formradiobutton_local.state = "1"
	self.container_local_state.visible = "1"