from class_acl_user import *

try:
	user = ACLUser.current()
	if not user.is_admin():
		self.visible = "0"
except Exception, ex:
	pass