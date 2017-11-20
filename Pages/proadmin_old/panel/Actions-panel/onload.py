from proadmin_utils import Utils

if Utils.is_admin():
	self.visible = '1'
else:
	self.visible = '0'