#30.01.2013 - last modification. Delete session
from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


def invoke_dispather( macros ):

	from VEE_vmacro_dispatcher import InvokeDispatcher
	from VEE_std_lib import v_currentpage

	invoke_disp = InvokeDispatcher()
	invoke_disp.page 		= self
	invoke_disp.growl 		= self.growl
	invoke_disp.xmldialog 	= self.xmldialog
	invoke_disp.macros 		= macros

	current_page = v_currentpage()
	current_page.page_name = self.name

	invoke_disp.current_page = current_page
	invoke_disp.run()


@authenticated
@administrator
@error_handler
def main():

	#macros invoked from macros
	object_guid = request.arguments.get( "macros_id" )
	if object_guid:
		from class_macro import Macros
		macros = Macros.get_by_guid( object_guid )
		if macros:
			invoke_dispather( macros )

main()
