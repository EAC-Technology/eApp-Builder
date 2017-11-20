import json
from vdom_trace import Trace
import managers
import localization


lang = localization.get_lang()
try:
	keyList = request.arguments.get( "keyList", "[]" )
	key = json.loads( keyList )[0]

	session["subject_keyList"] = key

	w_AclRules 	= session["w_AclRules"]

	w_AclRules.set_subject(key)
	w_AclRules.render(dt_rules = self.cnt_acls.cnt_rules.dt_rules)

except Exception:
	raise
	self.growl.action("show",[ lang["error"], lang["unknown_error"]])
