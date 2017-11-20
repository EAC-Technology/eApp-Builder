from templates import ResourceListTemplate
from models import Resource
from urls import reverse

app_id = request.arguments.get('id', '')
app_resources = Resource.filter(application_id=app_id)

self.hpt_resources.htmlcode = ResourceListTemplate(app_resources, add_new=True).html

self.cnt_res.dialog_create.form_create.application_id.value = app_id
self.cnt_res.dialog_update.form_update.application_id.value = app_id
