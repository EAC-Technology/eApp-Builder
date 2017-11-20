from templates import BreadcrumbTemplate
from models import Workspace, Application, Widget
from urls import reverse
from vdom_debug import p


try:
	script_name = request.environment.get('SCRIPT_NAME', '')
	pages = [dict(name='Home',is_active=True)]

	if script_name.startswith('/workspace'):
		workspace_id = request.arguments.get('id', '')
		workspace = Workspace.get(guid=workspace_id)
		if workspace:
			pages = [
				dict(
					name='Home',
					link=reverse('main')
				),
				dict(
					name=workspace.name,
					is_active=True
				),
			]
	elif script_name.startswith('/application'):

		app_id = request.arguments.get('id', '')
		app = Application.get(guid=app_id)
		if app:
			pages = [
				dict(
					name='Home',
					link=reverse('main')
				),
				dict(
					name=app.workspace.name,
					link=reverse('workspace', workspace_id=app.workspace_id)
				),
				dict(
					name=app.name,
					is_active=True
				),
			]

	elif script_name.startswith('/widget'):

		widget_id = request.arguments.get('id', '')
		widget = Widget.get(guid=widget_id)
		if widget:
			pages = [
				dict(
					name='Home',
					link=reverse('main')
				),
				dict(
					name=widget.workspace.name,
					link=reverse('workspace', workspace_id=widget.workspace_id)
				),
				dict(
					name=widget.name,
					is_active=True
				),
			]
	else:
		pages = [
			dict(
				name='Home',
				is_active=True
			)
		]

	self.hpt_breadcrumb.htmlcode = BreadcrumbTemplate(pages, many=True).html

except ImportError:
	response.redirect( "/logoff" )

except Exception, ex:
	from vdom_debug import p_ex

	p_ex()
