from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self

@authenticated
@administrator
@error_handler
def main( ):
	from widget_logger import WidgetLogs
	WidgetLogs.clear_log()
	self.dialog.cont_main.ctn_logs.htp_log.action( "setHTML", [ "" ] )


main()


