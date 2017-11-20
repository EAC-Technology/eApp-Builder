from models import View
from cgi import escape

view_id = request.arguments.get('view_id', '')
command = request.arguments.get('command', 'update')

app_view = View.get(guid=view_id)

if app_view:

	if command == 'play':
		# fill dov object with prerendered xml
		vdomxml, e2vdom = app_view.get_vdomxml()
		self.dialog_preview.dov_view.vdomxml = vdomxml
		self.dialog_preview.dov_view.vdomactions = e2vdom

		self.dialog_preview.show = '1'

	else:

		disabled = '2' if command == 'delete' else '0'

		form = self.dialog_update.form_update

		form.tab_view_detail.tab_params.input_title.value = app_view.name
		form.tab_view_detail.tab_params.input_title.mode = disabled
		form.tab_view_detail.tab_params.application_id.value = app_view.application_id
		form.tab_view_detail.tab_params.view_id.value = app_view.guid
		form.tab_view_detail.tab_params.command.value = command

		form.tab_view_detail.tab_layout.input_layout_xml.value = app_view.layout_xml or ""
#		form.tab_view_detail.tab_layout.input_layout_xml.mode = disabled

		form.tab_view_detail.tab_logic.input_logic_xml.value = escape(app_view.logic_xml or "")
		form.tab_view_detail.tab_logic.input_logic_xml.mode = disabled

		self.dialog_update.form_update.btn_update.label = command.title()
		self.dialog_update.form_update.tab_view_detail.tab_params.error_name.value = ''
		form.btn_update.action( "setClass", [ 'btn btn-danger' if command == 'delete' else 'btn btn-success' ] )
		self.dialog_update.title = 'View {}'.format(command.title())
		self.dialog_update.show = '1'
