from templates import (ACLViewTemplateCollection, ACLRoleTemplateCollection,
					   ACLRightTemplateCollection, ACLTableCollection)
from models import View, Role, Right, ACL
from collections import defaultdict

type = request.arguments.get('type', 'view')
object_id = request.arguments.get('object_id', '')
acl_table = session.get('acl_table')
acl_list = session.get('acl_list', {})

if type == 'view':
	view = View.get(guid=object_id)

	acl_views = acl_table.objects[0]
	acl_views.selected_id = view.guid
	acl_views.render()

	acl_roles = ACLRoleTemplateCollection()
	acl_roles.objects = view.roles
	view_role_acls = ACL.filter(object_id=view.guid)
	acl_roles.role_rights = defaultdict(int)
	for role_acl in view_role_acls:
		acl_roles.role_rights[role_acl.subject_id] += 1
	acl_roles.render()

	acl_table.objects = [acl_views, acl_roles]
	#role_rights

else:
	if type == 'role':

		if len(acl_table.objects) > 2:
			acl_table.objects = acl_table.objects[:-1]

		role = Role.get(guid=object_id)
		acl_table.objects[-1].selected_id = role.guid
		acl_table.objects[-1].render()
		selected_view = View.get(guid=acl_table.objects[0].selected_id)

		acl_rights = ACLRightTemplateCollection()
		acl_rights.objects = selected_view.rights
		acl_rights.selected_id = [acl.right_id for acl in acl_list.values() if acl.object_id == selected_view.guid and acl.subject_id == role.guid]
		acl_rights.view_rights = [acl.right_id for acl in selected_view.acl_list(role)]
		acl_rights.render()

		acl_table.objects.append(acl_rights)

	elif type == 'right':

		selected_right = Right.get(guid=object_id)

		# Update edited ACL list
		acl_instance = ACL(
			object_id=acl_table.objects[0].selected_id,
			subject_id=acl_table.objects[1].selected_id,
			right_id=selected_right.guid
		)
		if acl_instance.hash in acl_list:
			del acl_list[acl_instance.hash]
		else:
			acl_list[acl_instance.hash] = acl_instance

		session['acl_list'] = acl_list

		selected_view = View.get(guid=acl_table.objects[0].selected_id)
		selected_role = Role.get(guid=acl_table.objects[1].selected_id)

		acl_rights = acl_table.objects[-1]  # rights table
		acl_rights.selected_id = [acl.right_id for acl in acl_list.values() if acl.object_id == selected_view.guid and acl.subject_id == selected_role.guid]
#		acl_rights.view_rights = [acl.right_id for acl in selected_view.acl_list(selected_role)]
		acl_rights.render()
#		acl_table.objects[-1] = acl_rights


session['acl_table'] = acl_table.render()
self.hpt_acl.htmlcode = acl_table.html

display_buttons = '1' if bool(acl_list) else '0'
self.btn_cancel.visible = display_buttons
self.btn_apply.visible = display_buttons

# debug info
self.hpt_debug.action('setHTML', unicode(acl_table))
self.hpt_debug.action('addHTML', u"<br/>obj_count="+unicode(len(acl_table.objects)))
self.hpt_debug.action('addHTML', u"<br/>ids=[%s]" % ', '.join([unicode(obj.selected_id) for obj in acl_table.objects]))
self.hpt_debug.action('addHTML', u"<br/>acl_list_len=[%s]" % len(acl_list))
self.hpt_debug.action('addHTML', u"<br/>acl_list=[%s]" % '<br/>'.join([u"==> %s" % hash(obj) for obj in acl_list]))