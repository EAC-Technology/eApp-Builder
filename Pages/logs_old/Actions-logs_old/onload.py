from widget_user_group_dialog import authenticated, error_handler, administrator

@authenticated
@administrator
#@error_handler
def main( ):
	from widget_logger import WidgetLogsFilter, WidgetLogs

	WidgetLogsFilter.render( 	pluginDropDown = self.dialog.cont_main.cnt_filter.form.formlist,
								startDate	= self.dialog.cont_main.cnt_filter.form.s_date,
								startHour	= self.dialog.cont_main.cnt_filter.form.s_hour,
								startMinute = self.dialog.cont_main.cnt_filter.form.s_minute,
								endDate		= self.dialog.cont_main.cnt_filter.form.e_date,
								endHour		= self.dialog.cont_main.cnt_filter.form.e_hour,
								endMinute	= self.dialog.cont_main.cnt_filter.form.e_minute )


	widgetLogs = WidgetLogs()
	widgetLogs.render( self.dialog.cont_main.ctn_logs.htp_log )

	from widget_localization import LocalizationWidget
	loc_widget = LocalizationWidget()
	loc_widget.set_data( {
		"log_btn_hide_filter"			: self.dialog.cont_main.btn_filter_hide,
		"log_btn_show_filter"			: self.dialog.cont_main.btn_filter_show,
		"log_btn_clear_log"				: self.dialog.cont_main.btn_clear,
		"log_btn_refresh_log"			: self.dialog.cont_main.btn_refresh,
		"log_filter_text"				: self.dialog.cont_main.cnt_filter.text_filter,
		"log_by_time"					: self.dialog.cont_main.cnt_filter.form.formcheckbox_time,
		"log_by_plugin_macros"			: self.dialog.cont_main.cnt_filter.form.text_plugin,
		"log_btn_reset_filter"			: self.dialog.cont_main.cnt_filter.form.btn_reset,
		"log_btn_apply_filter"			: self.dialog.cont_main.cnt_filter.form.btn_apply,
	})

	loc_widget.render()


main()
