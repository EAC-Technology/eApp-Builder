import json
from vdom_trace import Trace
import managers


#try:
if True:
	keys = session.get("rules_orig",None)

	w_AclRules 		= session["w_AclRules"]
	w_AclRules.render(dt_rules = self.cnt_acls.cnt_rules.dt_rules)

#except Exception, ex:
#	for key in session.keys():
#		del session[key]
#	session[ "error" ] = unicode("Server encountered an error. Please, contact with your administrator or check the information log.")
#	managers.log_manager.info_bug(
#		u"ProAdmin error: %s" % Trace.exception_trace(5),
#		u"ProAdmin %s" % self.name
#	)
#	self.action("goTo",["/login"])
