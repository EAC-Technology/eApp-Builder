try:

	import ProAdmin
	import localization
	from utilities import current_page_name, get_logout_back_url
	from widget_localization import LocalizationWidget
	from class_license import License
	import json
	from collections import OrderedDict
	from proadmin_remote_settings import RemoteSettings
	from proadmin_sso import SSOUrl
	from config import proshare_config


	lang = localization.get_lang()

	# menu highlighting
	page_name = current_page_name().lower()
	macros_list = ["macros_settings", "create_macros", "edit_macros", "plugin_details", "plugins", "macros_source"]
	main_list = ['main', 'workspace', 'application', 'widget']
	settings_list = ['settings', 'users_and_groups', 'plugins', 'remote_scheme',]
	logs_list = ['logs']

	if page_name in main_list:
		self.menu_main.classname += " m-active"
	elif page_name in settings_list:
		self.menu_settings.classname += " m-active"
	elif page_name in page_name:
		self.menu_logs.classname += " m-active"
	else:
		self.menu_settings.classname += " m-active"

	if not License().confirmed:
		response.redirect("/license.vdom")

	# get back url
	back_url = get_logout_back_url()

	user = ProAdmin.current_user()
	if not user:
		response.redirect( '/login?back_url=%s' % back_url )

	self.cont_login.text_login.value = user.name

	if not ProAdmin.application().rules( user, 'a' ):
		self.menu_settings.visible = '0'
		#self.menu_macros.visible = '0'

	list_html = "<div class='top_start_container'></div>"
	if RemoteSettings.get_remote_settings():
		# define current protocol
		protocol = SSOUrl.current_protocol() or 'http'

		list_html += "<div class='first_block block_start_container'><div class='center_align_block switch-to'>"+lang.get("switch_to", "Switch to")+"</div></div>"
		apps = ProAdmin.get_registred_applications()
		current_app_host = ProAdmin.hosts()
		for a in apps:
			if "b0a274f0-22bc-44be-be48-da6ec9180268" != apps[a]["guid"] and current_app_host != apps[a]["hosts"]:
				app_host = apps[a]["hosts"][0] if "hosts" in apps[a] else ""

				# add protocol to application url
				if app_host:
					app_host = protocol + '://' + app_host

				app_img = ""
				if "491d4c93-4089-4517-93d3-82326298da44" == apps[a]["guid"]:
					app_img = "/c5150260-6e53-4c1b-a853-b42828b1925a.res"
				elif "526ae088-8004-469c-9d8e-cea715f8f63b" == apps[a]["guid"]:
					app_img = "/b358eb6f-1163-4d27-942d-150be8c2967a.res"
				elif "fc2221b2-794b-4c40-991f-6c7c2f61dbc2" == apps[a]["guid"]:
					app_img = "/44e72c66-9b9e-42f4-b5b3-78e8c463f598.res"
				elif "22d43054-9861-48e8-875f-53d09bb1fd11" == apps[a]["guid"]:
					app_img = "/aad0d263-0f83-46b7-884e-c3c67370f237.res"
				elif "7f459762-e1ba-42d3-a0e1-e74beda2eb85" == apps[a]["guid"]:
					app_img = "/04ef9182-d5cd-46f3-9fab-cf602914ea3e.res"
				elif "b0a274f0-22bc-44be-be48-da6ec9180268" == apps[a]["guid"]:
					app_img = "/48e42a4a-c4cb-49d3-9e8a-02d85c8fd348.res"

				list_html += "<div class='app_start_container'><div class='center_align_app' title='" + app_host + "'><img src='" + app_img + "'><a href='" + app_host + "'>" + apps[a]["name"] + "</a></div></div>"

	first_block = "first_block" if not RemoteSettings.get_remote_settings() else ""
	list_html += "<div class='" + first_block + " block_start_container'><div class='center_align_block current-user'>" + user.name + "</div></div>"
	list_html += "<div class='block_start_container app-like'><div class='center_align_block'><img src='/78706468-3987-4c22-9b80-67ae68cbd3db.res'><a href='/logoff.vdom'>"+lang.get("logout", "Log Out")+"</a></div></div><div class='bottom_start_container'></div>"

	self.container_start.hpt_start.htmlcode = list_html
	self.button_start.hint = "{0} {1}".format(application.name, proshare_config["version"])


	localization = LocalizationWidget()
	localization.add_controls( 'menu_settings_title', self.menu_settings.title )
	localization.add_controls( 'menu_builder_title', self.menu_main.title )

	localization.render()
except ImportError:
	response.redirect( "/logoff" )

except Exception, ex:
	from app_settings import settings
	error_text = lang['unknown_error']

	if settings.TEST_MODE:
		from vdom_trace import Trace
		error_text = Trace.exception_trace()

	self.growl.title = lang["error"]
	self.growl.text = error_text
	self.growl.active = "1"
