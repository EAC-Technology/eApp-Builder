from templates import RoleTemplateCollection, RightTemplateCollection
from models import Application, Role, Right

app_id = request.arguments.get('id', '')

app = Application.get(guid=app_id)

roles = Role.filter(workspace_id=app.workspace_id)
rights = Right.filter(workspace_id=app.workspace_id)

self.hpt_roles.htmlcode = RoleTemplateCollection(roles, many=True, add_new=True).html
self.hpt_roles.htmlcode += RightTemplateCollection(rights, many=True, add_new=True).html

self.cnt_role.dialog_create.form_create.workspace_id.value = app.workspace_id
