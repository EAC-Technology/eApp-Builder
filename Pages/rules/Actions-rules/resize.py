from vdom_trace import Trace
import managers
from widget_localization import LocalizationWidget

try:
	# resizing
	args = request.arguments
#	self.cnt_acls.cnt_rules.height 	= self.cnt_acls.cnt_subjects.height = self.cnt_acls.cnt_tree.height = int(args["height"]) - 90
#	new_width = int(args["width"])
#	if new_width > 1300:
#		self.cnt_acls.cnt_rules.width 	= int(args["width"]) * 0.453 	# O_o коэффициент корреляции дислокации
#	else:
#		self.cnt_acls.cnt_rules.width 	= int(args["width"]) * 0.43 	# o_O коэффициент корреляции перегенерации

#	if app:
#		# Application objects (TREE-view)
#		WidgetAclObjects = WidgetAclObjects()
#		WidgetAclObjects.set_app(app)
#		WidgetAclObjects.render(self.cnt_acls.cnt_tree.app_structure)
#		session["WidgetAclObjects"] = WidgetAclObjects
#		w_AclRules 		= session.get("w_AclRules")
#		w_AclSubjects 	= session.get("w_AclSubjects")
#
#		if w_AclSubjects:
#			w_AclSubjects.render( dt_subjects  = self.cnt_acls.cnt_subjects.dt_subjects	)
#
#		if w_AclRules:
#			w_AclRules.render(dt_rules = self.cnt_acls.cnt_rules.dt_rules)
#
#	else:
#		raise RemoteApplicationDisconnected()


except AccessDeniedError, ex:
	session[ "error" ] = unicode(ex)
	response.redirect("/login")

except AuthorisationError, ex:
	session[ "error" ] = unicode(ex)
	response.redirect("/login")

except RemoteApplicationDisconnected, ex:
	session[ "error" ] = unicode(ex) % guid
	response.redirect("/login")

#except Exception, ex:
#	for key in session.keys():
#		del session[key]
#	session[ "error" ] = unicode("Server encountered an error. Please, contact with your administrator or check the information log.")
#	managers.log_manager.info_bug(
#		u"ProAdmin error: %s" % Trace.exception_trace(5),
#		u"ProAdmin %s" % self.name
#	)
#	self.action("goTo",["/login"])


#from widget_localization import LocalizationWidget
#localization = LocalizationWidget()
#
#localization.add_controls( 'cont_rules_title', self.cnt_acls.cnt_rules )
#localization.add_controls( 'cont_subjects_title', self.cnt_acls.cnt_subjects )
#localization.add_controls( 'cont_tree_title', self.cnt_acls.cnt_tree )
#localization.add_controls( 'rules_acl_apply_btn', self.cnt_toolbar.btn_apply )
#localization.add_controls( 'rules_acl_cancel_btn', self.cnt_toolbar.btn_reset )
#localization.render()
