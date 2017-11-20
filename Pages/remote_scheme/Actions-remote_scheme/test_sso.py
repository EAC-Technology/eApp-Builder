from proadmin_sso import SSOClient
import localization
lang = localization.get_lang()

try:
	sender = request.arguments.get("sender", "")
	host = ""
	if sender == "8c9c80d7-8d0c-43a1-956b-40f646e4f554":
		host = request.shared_variables["host"]
		if not host:
			raise
	ssoclient = SSOClient( request, response )
	ssoclient.set_action_mode( self )

	ssoclient.test_sso( url=host )

	session["sso_tested"] = "1"
except Exception, ex:
	self.growl.action("show", [lang["error_title"], lang["fill_all_fields_error"]])