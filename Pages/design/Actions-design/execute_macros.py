#30.01.2013 - last modification. Delete session
from widget_user_group_dialog import authenticated, error_handler
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


def invoke_dispather( macros ):

	from VEE_vmacro_dispatcher import InvokeDispatcher
	from VEE_proplanning_lib import v_proplanning_home_page
	from datetime import datetime
	from user_settings import get_visible_calendars
	import ProAdmin

	invoke_disp = InvokeDispatcher()
	invoke_disp.page 		= self
	invoke_disp.growl 		= self.growl1
	invoke_disp.xmldialog 	= self.xmldialog
	invoke_disp.macros 		= macros

	current_page = v_proplanning_home_page()
	start,end =  request.shared_variables[ 'start_end' ].split( ":" )
	current_page.time_inteval = ( datetime.fromtimestamp( float(start) ), datetime.fromtimestamp( float(end) ) )
	current_page.selected_calendars = get_visible_calendars( ProAdmin.current_user().guid )
	current_page.calendar_view = request.shared_variables[ 'view' ]
	current_page.page_name 		= self.name

	invoke_disp.current_page = current_page
	invoke_disp.run()


@authenticated
#@error_handler
def main():

	from class_macro import Macros

	#click on macros\plugiuns panel
	object_guid = request.arguments.get( "id" )
	if object_guid:

		if object_guid.find( "_", 0 ) == 1:
			#parse guid
			prefix, object_guid = object_guid.split( "_", 1 )
			#check prefix value

			if prefix == "p": #it is plugin guid

				from widget_macros_datatable import WidgetMacrosDatatable
				widget_macro_table = WidgetMacrosDatatable( object_guid, self.name )
				widget_macro_table.render( 	self.dialog_plugin_macros.datatable,\
											self.dialog_plugin_macros )

				self.dialog_plugin_macros.show = "1"
				return

			elif prefix <> "m":
				raise Exception( "Unknown GUID" )

	#click from dialog_plugin_macros.datatable
	elif request.arguments.get( "keyField" ):
		object_guid = request.arguments.get( "keyField" )

	#macros invoked from macros
	elif request.arguments.get( "macros_id" ):
		object_guid = request.arguments.get( "macros_id" )

	else:
		raise Exception( "Bad GUID" )

	macros = Macros.get_by_guid( object_guid )
	if not macros:
		raise Exception( "Bad GUID" )

	invoke_dispather( macros )


main()
