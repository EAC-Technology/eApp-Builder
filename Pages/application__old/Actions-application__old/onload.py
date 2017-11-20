try:
	import localization
	from widget_localization import LocalizationWidget

	from models import Application
	from urls import reverse

	lang = localization.get_lang()

	if not 'id' in request.arguments:
		response.redirect(reverse('main'))

	app_id = request.arguments.get('id')
	app = Application.get(guid=app_id)

	if not app:
		response.redirect(reverse('main'))


except Exception, ex:
	from app_settings import settings
	from vdom_debug import p_ex

	if settings.TEST_MODE:
		p_ex()

	self.growl.title = lang['error']
	self.growl.text = lang['unknown_error']
	self.growl.active = "1"