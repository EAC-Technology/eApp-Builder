session['acl_list'] = {}
self.btn_cancel.visible = '0'
self.btn_apply.visible = '0'

acl_table = session.get('acl_table')
if acl_table:
	acl_table.objects = acl_table.objects[:1]
	acl_table.objects[0].selected_id = 0
	acl_table.objects[0].render()
	acl_table.render()
	self.hpt_acl.htmlcode = acl_table.html

	session['acl_table'] = acl_table
