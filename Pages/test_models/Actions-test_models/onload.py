"""
	Test page
"""
from models import Workspace, Application, Widget, View, Resource, DataSource
from app_settings import settings
import json
from cgi import escape


def print_data(title, list=None, br=True):
	if br:
		response.write('<br/>------<br/>', True)
	response.write('<br/>{}:<br/>'.format(title.upper()), True)
	if list is not None:
		response.write('[%s]' % ', <br/>'.join([str(list_obj) for list_obj in list]), True )

def workspace_test():
	print_data('workspaces objects', br=False)

	for index in range(3):
		w = Workspace()
		w.name = 'New workspace name'
		w.description = 'Some new description'
		w.save()

	workspaces = Workspace.all()
	print_data('new objects -> model.all()', workspaces)

	w.name = 'Updated name'
	w.save()

	workspaces = Workspace.all()
	print_data('UPDATED -> model.all()', workspaces)

	workspaces = Workspace.get(id=w.id, name=w.name)
	print_data('GET -> model.get()', [workspaces])

	workspaces = Workspace.filter(name='New workspace name')
	print_data('FILTER -> model.filter()', workspaces)

	for index in range(2):
		o = Application()
		o.workspace_id = w.guid
		o.save()

	a = View()
	a.application_id = o.guid
	a.save()

	a = Resource()
	a.application_id = o.guid
	a.save()

	for index in range(3):
		o = Widget()
		o.workspace_id = w.guid
		o.save()

	for index in range(3):
		o = DataSource()
		o.workspace_id = w.guid
		o.save()

	objects = Workspace.all() + Resource.all() + Application.all() + Widget.all() + DataSource.all() + View.all()
	print_data('All objects in db', objects)

#	[w.delete() for w in Workspace.all()]
	workspaces = Workspace.all()
	print_data('cleaned', workspaces)

	workspaces = Workspace.filter(include_deleted=True)
	print_data('cleaned with deleted if exists', workspaces)

	objects = Workspace.all() + Resource.all() + Application.all() + Widget.all() + DataSource.all() + View.all()
	print_data('no objects left', objects)

def application_test():
	pass

def view_test():
	pass

def widget_test():
	print_data('widgets objects', br=False)
	workspaces = []
	for index in range(3):
		w = Workspace()
		w.name = 'New workspace name'
		w.description = 'Some new description'
		w.save()
		workspaces.append(w)

	for index in range(3):
		w = Widget()
		w.source = '<source>some stuff</source>'
		w.workspace_id = workspaces[0].guid if index in [0, 1] else workspaces[1].guid
		w.save()

	widgets = Widget.all()
	print_data('new objects -> model.all()', widgets)

	w.source = '<b>UDPATED</b>'
	w.save()
	w.reload()

	print_data('UPDATED', [w.source])

	widgets = Widget.get(id=w.id)
	print_data('GET -> model.get()', [widgets])

	widgets = Widget.filter(source='<source>some stuff</source>')
	print_data('FILTER -> model.filter()', widgets)

	for index, w in enumerate(workspaces):
		widgets = w.widgets
		print_data('workspace %s -> workspace.widgets' % str(index), widgets)

	[w.delete() for w in Widget.all()]
	objects = Widget.all() + Workspace.all()
	print_data('cleaned', objects)

	widgets = Widget.filter(include_deleted=True)
	print_data('cleaned with deleted if exists', widgets)

def data_source_test():
	pass

def resource_test():
	pass

if not settings.TEST_MODE:
	response.redirect('/main')

try:

#	workspace_test()
#	application_test()
#	widget_test()
#	data_source_test()
#	view_test()
#	resource_test()

	workspaces_json = { "workspaces": [w.to_json() for w in Workspace.all()] }

#	print_data("JSONs", workspaces_json["workspaces"])
	response.write( escape(json.dumps(workspaces_json, sort_keys=True, indent=4)) )




except Exception, ex:
	from app_settings import settings
	from vdom_debug import p_ex

	if settings.TEST_MODE:
		p_ex()
