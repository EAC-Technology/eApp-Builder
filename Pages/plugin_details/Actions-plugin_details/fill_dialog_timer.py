from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

	from class_timer import Timer
	timer_id = request.shared_variables["timer_id"]
	if timer_id:
		self.dialog_add_timer.form_add_timer.formtext_id.value = timer_id
		timer = Timer.get_by_id(timer_id)
		self.dialog_add_timer.form_add_timer.formtext_name.value = timer.name
		self.dialog_add_timer.form_add_timer.formtext_period.value = timer.period
	else:
		self.dialog_add_timer.form_add_timer.formtext_id.value = ""
		self.dialog_add_timer.form_add_timer.formtext_name.value = ""
		self.dialog_add_timer.form_add_timer.formtext_period.value = "00:00:00:00"


main()
