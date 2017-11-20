from config import proshare_config
from class_license import License
from widget_localization import LocalizationWidget
from proadmin_sso import ClientLoginHelper
from VEE_core import engine #only for Engine initialization
import localization, ProAdmin
from app_settings import settings

##############Auto Login###############


auto_login = settings.DEVELOP_AUTOLOGIN
if auto_login:
	# create fake request
	class Fake( object ):
		def __init__( self ):
			self.arguments = {}

	fake = Fake()

	# copy arguments
	for key in request.arguments.keys():
		value = request.arguments.get( key )
		fake.arguments[ key ] = value if value else None

	# replace login and password
	fake.arguments[ 'login' ] = settings.DEV_LOGIN
	fake.arguments[ 'password' ] = settings.DEV_PASSWORD

	# replace request by fake request
	request = fake

########################################

if not License().confirmed:
	response.redirect("/license")

if "version" in proshare_config and proshare_config[ "version" ]:
	self.dialog_login.text_version.value = "v. " + proshare_config[ "version" ]

if "error" in session:
	self.growl.title = "Error"
	self.growl.text = session[ "error" ]
	self.growl.active = "1"
	del session[ "error" ]

# -----------------------------------------------------------------
#		LOGIN
# -----------------------------------------------------------------

login_helper = ClientLoginHelper( request, response , back_url="/")

lang = localization.get_lang()

try:
	login_helper.login_by_token()

	login_helper.login_by_proadmin()

	login_helper.login_by_password()



except ProAdmin.ProAdminEmptyPasswordError, ex:
	self.growl.title = lang["error"]
	self.growl.text = lang["empty_password_error"]
	self.growl.active = "1"

except ProAdmin.ProAdminEmptyLoginError, ex:
	self.growl.title = lang["error"]
	self.growl.text = lang["empty_login_error"]
	self.growl.active = "1"

except ProAdmin.ProAdminLoginError, ex:
	self.growl.title = lang["error"]
	self.growl.text = lang["invalid_login_or_password_error"]
	self.growl.active = "1"

#except Exception, ex:
#	self.growl.title = lang["error"]
#	self.growl.text = unicode( ex )
#	self.growl.active = "1"



# -----------------------------------------------------------------
#		LOCALIZATION
# -----------------------------------------------------------------


localization = LocalizationWidget()
localization.add_controls( 'login_page_title', self )
localization.add_controls( 'login', self.dialog_login.form_login.text_login )
localization.add_controls( 'password', self.dialog_login.form_login.text_password )
localization.render()
