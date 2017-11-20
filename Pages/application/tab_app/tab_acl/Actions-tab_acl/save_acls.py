from models import View, ACL
from collections import defaultdict

acl_list = session.get('acl_list', {})

for key, acl_instance in acl_list.items():
	acl_instance.save()

session['acl_list'] = {}
self.btn_cancel.visible = '0'
self.btn_apply.visible = '0'

acl_table = session.get('acl_table')
if acl_table:
	acl_rights = acl_table.objects[-1]
	acl_rights.selected_id = []
	selected_view = View.get(guid=acl_table.objects[0].selected_id)
	acl_rights.view_rights = [acl.right_id for acl in selected_view.acl_list(acl_table.objects[1].selected_id)]
	acl_rights.render()

	acl_roles = acl_table.objects[1]

	view_role_acls = ACL.filter(object_id=selected_view.guid)
	acl_roles.role_rights = defaultdict(int)
	for role_acl in view_role_acls:
		acl_roles.role_rights[role_acl.subject_id] += 1
	acl_roles.render()

	acl_table.render()
	self.hpt_acl.htmlcode = acl_table.html

	session['acl_table'] = acl_table
