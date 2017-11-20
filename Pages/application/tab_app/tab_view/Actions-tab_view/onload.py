from templates import ViewTemplateCollection
from models import View

app_id = request.arguments.get('id', '')

app_views = View.filter(application_id=app_id)

self.hpt_views.htmlcode = ViewTemplateCollection(app_views, many=True, add_new=True).html

self.cnt_view.dialog_create.form_create.application_id.value = app_id
