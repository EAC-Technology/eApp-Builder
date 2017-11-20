import ProAdmin
import localization
from class_license import License
from utilities import get_logout_back_url


if not License.confirmed:
	response.redirect("/license.vdom")
lang = localization.get_lang()
self.title = lang["clear_page_title"]

try:
	# check admin rights
	user = ProAdmin.current_user()


	if not user:
		raise Exception()

	if not ProAdmin.application().rules( user, 'a' ):
		raise Exception()
except:
	back_url = get_logout_back_url()
	response.redirect( '/logoff?back_url=%s' % back_url )
