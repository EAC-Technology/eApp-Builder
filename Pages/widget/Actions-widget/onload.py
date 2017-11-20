try:
	import localization

	from models import Widget
	from urls import reverse

	lang = localization.get_lang()

	if not 'id' in request.arguments:
		response.redirect(reverse('main'))

	widget_id = request.arguments.get('id', '')
	widget = Widget.get(guid=widget_id)

	if not widget:
		response.redirect(reverse('main'))

	self.title = u"Widget : {}".format(widget.name)

	self.form_widget.code_widget.value = widget.source
	self.form_widget.widget_id.value = widget.guid

except Exception, ex:
	from app_settings import settings
	from vdom_debug import p_ex

	if settings.TEST_MODE:
		p_ex()

	self.growl.title = lang['error']
	self.growl.text = lang['unknown_error']
	self.growl.active = "1"
