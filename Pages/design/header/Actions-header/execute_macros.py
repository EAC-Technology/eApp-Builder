from class_macros import Macros
from vscript import errors, generic, boolean, string, v_empty, v_true_value, v_false_value, as_string, engine
from vscript.subtypes import *
from vscript.variables import *
from vscript.conversions import *
from VEE_vmacro_dispatcher import v_logger, v_xml_dialog, v_page_status, v_http_request

xml_dialog = v_xml_dialog()
page_status = v_page_status()
http_request = v_http_request()

macros_id = ""
if request.arguments:
	arg_dict = {}
	for key in request.arguments.keys():
		if key != "sender":
			arg_dict[key] = request.arguments.get(key)
	xml_dialog.answer(arg_dict)

if "id" or "macros_id" in request.arguments:
	macros_id = request.arguments.get("id") if "id" in request.arguments else request.arguments.get("macros_id")

if "selected_contacts" in session and session.get("selected_contacts"):
	page_status.set_contact_list(session.get("selected_contacts"))

self.xmldialog.action("hide", [])
if macros_id:
	try:
		macros = Macros.get_by_id(macros_id)
		cmpl = engine.vcompile(macros.code)

		if not cmpl[1]:
			raise Exception("Vscript is not compiled")

		vscript_wrappers_name="wrappers"
		vscript_extentions_name = "vscript"

		xml_dialog.set_macros_id(macros_id)


		server.vscript.execute(macros.code,
		**{
		"logger" 		: v_logger().v_log,
		"xml_dialog"	: xml_dialog,
		"page_status"	: page_status,
		"http_request"	: http_request,
		"dictionary"	: vscript_extentions_name,
		"vdomdbconnection": vscript_wrappers_name,
		"wholeconnection": vscript_wrappers_name, "wholeapplication": vscript_wrappers_name,
		"wholeerror": vscript_wrappers_name, "wholeconnectionerror": vscript_wrappers_name, "wholenoconnectionerror": vscript_wrappers_name,
		"wholeremotecallerror": vscript_wrappers_name, "wholeincorrectresponse": vscript_wrappers_name,
		"wholenoapierror": vscript_wrappers_name, "wholenoapplication": vscript_wrappers_name,
		})

		if xml_dialog.get_answer() or request.arguments or page_status.get_contact_list():
			self.xmldialog.action("show", [])
			self.xmldialog.action("loadData", [xml_dialog.show_xml_form()])


	except Exception, ex:
	#	self.growl.action("show", ["Error", "Macros id is not defined"])
		self.growl.action("show", ["Error", str(ex)])
