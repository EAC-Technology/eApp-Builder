from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self

@authenticated
@administrator
@error_handler
def main( ):

	args = request.arguments
	allow = True
	start = end = None

	if args.get( "formcheckbox_time", None ):

		from datetime import datetime
		import localization
		lang = localization.get_lang()

		s_date 		= args.get( "s_date"	, "" )
		e_date 		= args.get( "e_date"	, "" )
		s_hour 		= args.get( "s_hour"	, "" )
		s_minute 	= args.get( "s_minute"	, "" )
		e_hour 		= args.get( "e_hour"	, "" )
		e_minute 	= args.get( "e_minute"	, "" )

		format_string = "%Y-%m-%d %H:%M"

		try:
			start = datetime.datetime.strptime( "{0} {1}:{2}".format( s_date, s_hour, s_minute ), format_string )
		except:
			self.growl.action( "show", [ lang.get( "log_error", "Error" ), lang.get( "log_invalid_start_date", "Invalid start date" ) ] )
			allow = False

		try:
			end = datetime.datetime.strptime( "{0} {1}:{2}".format( e_date, e_hour, e_minute ), format_string )
		except:
			self.growl.action( "show", [ lang.get( "log_error", "Error" ), lang.get( "log_invalid_end_date", "Invalid end date" ) ] )
			allow = False

		if end and start and end <= start:
			self.growl.action( "show", [ lang.get( "log_error", "Error" ), lang.get( "log_invalid_start_end", "Start date must be less then end date" ) ] )
			allow = False


	if allow:

		from widget_logger import create_log_filter, WidgetLogs
		filter = None

		object_guid = args.get( "formlist", "all" )

		if object_guid != "all":
			if object_guid[0] == "p":
				filter = create_log_filter( plugin_guid = object_guid[1:], start = start, end = end )
			elif object_guid[0] == "m":
				filter = create_log_filter( macros_guid = object_guid[1:], start = start, end = end )
		elif end and start:
			filter = create_log_filter(  start = start, end = end )


		widgetLogs = WidgetLogs( filter )
		widgetLogs.render( self.dialog.cont_main.ctn_logs.htp_log, True )

		#self.action( "custom", [ """jQuery("div#o_{id}").scrollTop(999);""".format( id = self.dialog.cont_main.ctn_logs.htp_log.id.replace("-","_") ) ] )
		self.dialog.cont_main.cnt_filter.action( "hide", [""] )
		self.dialog.cont_main.btn_filter_hide.action( "hide", [""] )
		self.dialog.cont_main.btn_filter_show.action( "show", [""] )


main()
