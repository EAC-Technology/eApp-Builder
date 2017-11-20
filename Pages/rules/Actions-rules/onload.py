from class_license import License

if not License.confirmed:
	response.redirect("/license.vdom")
from class_acl_user import ACLUser
from widget_acl_objects import WidgetAclObjects
from class_errors import AccessDeniedError, AuthorisationError, RemoteApplicationDisconnected
import ProAdmin
import managers
from vdom_trace import Trace
import localization

lang = localization.get_lang()
try:
	user = ACLUser.current()

	if not user or not user.is_admin():
		raise AccessDeniedError()

	app = ProAdmin.application()

	if app:
		# Application objects (TREE-view)
		WidgetAclObjects = WidgetAclObjects()
		WidgetAclObjects.set_app(app)
		WidgetAclObjects.render(self.cnt_acls.cnt_tree.app_structure)
		session["WidgetAclObjects"] = WidgetAclObjects
#		w_AclRules 		= session.get("w_AclRules")
#		w_AclSubjects 	= session.get("w_AclSubjects")
#
#		if w_AclSubjects:
#			w_AclSubjects.render( dt_subjects  = self.cnt_acls.cnt_subjects.dt_subjects	)
#
#		if w_AclRules:
#			w_AclRules.render(dt_rules = self.cnt_acls.cnt_rules.dt_rules)

	else:
		raise RemoteApplicationDisconnected()




except Exception, ex:
	self.growl.title = lang["error"]
	self.growl.text = lang["unknown_error"]
	self.growl.active = "1"



from widget_localization import LocalizationWidget
localization = LocalizationWidget()

localization.add_controls( 'rules_management_page_title', self )
localization.add_controls( 'cont_rules_title', self.cnt_acls.cnt_rules )
localization.add_controls( 'cont_subjects_title', self.cnt_acls.cnt_subjects )
localization.add_controls( 'cont_tree_title', self.cnt_acls.cnt_tree )
localization.add_controls( 'rules_acl_apply_btn', self.cnt_toolbar.btn_apply )
localization.add_controls( 'rules_acl_cancel_btn', self.cnt_toolbar.btn_reset )
localization.render()
