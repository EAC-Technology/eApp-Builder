
from utils_base_classes import TemplateCollection
from urls import reverse_api

UPLOADER_JS = u"""

"""

UPLOADER_HTML = u"""

<form class="upload-form" id="resource-form-create">
	<input id="image" type="file" name="res_file"/>
</form>

<script>
	{script_js}
</script>

"""

class ViewTemplateCollection(TemplateCollection):
	template = UPLOADER_HTML


	def context(self, uploader):
		return dict(
			script_js=UPLOADER_JS
		)

