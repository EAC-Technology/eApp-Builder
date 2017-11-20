from templates import ScriptTemplateCollection
from models import AppScript

app_id = request.arguments.get('id', '')

app_scripts = AppScript.filter(application_id=app_id)

self.hpt_scripts.htmlcode = ScriptTemplateCollection(app_scripts, many=True, add_new=True).html

self.cnt_script.dialog_create.form_create.application_id.value = app_id
