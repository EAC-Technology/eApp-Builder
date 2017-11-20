from templates import (ACLViewTemplateCollection, ACLRoleTemplateCollection,
					   ACLRightTemplateCollection, ACLTableCollection)
from models import Application

app_id = request.arguments.get('id', '')

app = Application.get(guid=app_id)

workspace = app.workspace

app_views = ACLViewTemplateCollection(app.views)
acl_table = ACLTableCollection([app_views])

session['acl_table'] = acl_table
session['acl_list'] = {}
self.hpt_acl.htmlcode = acl_table.html