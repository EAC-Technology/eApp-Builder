import ProAdmin

# check user
user = ProAdmin.current_user()
if user:
	response.redirect( '/main' )
else:
	response.redirect( '/login' )
