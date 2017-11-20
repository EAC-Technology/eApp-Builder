from models import Workspace, Widget
from urls import reverse

if 'widget_id' not in request.arguments:
	raise Exception(u'Widget ID is not provided')

widget_id = request.arguments['widget_id']
widget = Widget.get(guid=widget_id)

if widget:
	widget.source = request.arguments['code_widget']
#	widget.set_xml(request.arguments['code_widget'])
	widget.save()

	self.growl.action('show', ["Saved", "Widget has been updated"])
