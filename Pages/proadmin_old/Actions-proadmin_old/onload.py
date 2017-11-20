from proadmin_utils import Utils


class SilenException( Exception ):
	pass



try:
	# process ping command
	if 'ping' in request.arguments:
		response.write( Utils.ping(), True )
		raise SilenException()

	# check admin rights
	if not Utils.is_admin():
		self.login_dialog.show = '1'
	else:
		self.login_dialog.show = '0'


except SilenException:
	pass