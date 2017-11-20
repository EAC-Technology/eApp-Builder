from proadmin_sso import SSOUrl
import ProAdmin

back_url = session.get( 'back_url', '' )

login_path = '/login'
if back_url:
	login_path = '/login?back_url=%s' % back_url
	del session[ 'back_url' ]

# local scheme
url = login_path

# remote scheme
if ProAdmin.scheme().is_remote():
	app_host = SSOUrl.current_protocol() + '://' + SSOUrl.current_host()

	url = SSOUrl.proadmin_url( '/logoff' )
	url.cont_url = app_host + login_path
	url = url.build()

# redirect
self.action( "goTo", url )
