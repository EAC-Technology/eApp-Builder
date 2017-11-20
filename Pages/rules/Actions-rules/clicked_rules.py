import json
import managers
from vdom_trace import Trace
import localization


lang = localization.get_lang()
try:

	keyList = request.arguments.get( "keyList", "[]" )
	keys = json.loads( keyList )

	session["rules_keysList"] 	= keys
except Exception:
	self.growl.action("show",[ lang["error"], lang["unknown_error"]])
#except Exception, ex:
#	for key in session.keys():
#		del session[key]
#	session[ "error" ] = unicode("Server encountered an error. Please, contact with your administrator or check the information log.")
#	managers.log_manager.info_bug(
#		u"ProAdmin error: %s" % Trace.exception_trace(5),
#		u"ProAdmin %s" % self.name
#	)
#	self.action("goTo",["/login"])
