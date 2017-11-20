#last modification 12.10.2012
#full refactoring

from widget_user_group_dialog import authenticated,administrator,error_handler,\
local_scheme, country_list_str


import ProAdmin
if ProAdmin.scheme().is_remote():
	response.redirect( '/proadmin_attention' )


@authenticated
@administrator
@local_scheme
@error_handler
def main():

	from widget_user_and_group_datatable import WidgetUserAndGroupDatatable
	import widget_user_and_group_dd_group

	response.shared_variables[ "currentTab" ] = "users"
	widgetUGDatatable = WidgetUserAndGroupDatatable( current_tab = "users" )
	widgetUGDatatable.render( self.cont.dt_main, self.pager, self.cont.error_text )
	widget_user_and_group_dd_group.render( self.form.obj_from_group )


main()

self.js_functions.htmlcode = self.js_functions.htmlcode.format(

	new_sf_name_id  = self.dialog_add_to_group.form_add_to_group.new_group_name.id.replace( "-", "_" ),
	page_id = self.id.replace( "-", "_" ),
	password_id = self.dialog_user.user_form.password_input.id.replace( "-", "_" ),
	visible_password_id = self.dialog_user.user_form.visible_password_input.id.replace( "-", "_" ),
	continue_input_id = self.dialog_user.user_form.continue_input.id.replace( "-", "_" ),
	user_form_id = self.dialog_user.user_form.id.replace( "-", "_" ),
			)


self.dialog_user.user_form.cont.country_input.value = country_list_str


from widget_localization import LocalizationWidget
localization = LocalizationWidget()
localization.set_data( {
		"users_groups_management_title" 		: self.page_title,
		"users_groups_management_page_title" 	: self,
		"create_user_btn_text"					: self.btn_create_user,
		"add_selected_to_group_btn_text"		: self.btn_add_to_group,
		"create_group_btn_text"					: self.btn_create_group,
		"users_tab_title"						: self.tabview1.cont_user,
		"groups_tab_title"						: self.tabview1.cont_group,
		"dialog_create_user_title"				: self.dialog_user.new_user_text,
		"dialog_edit_user_title"				: self.dialog_user.edit_user_text,
		"login_field_title"						: self.dialog_user.user_form.login_text,
		"password_field_title"					: self.dialog_user.user_form.password_text,
		"last_name_field_title"					: self.dialog_user.user_form.cont.ln_text,
		"first_name_field_title"				: self.dialog_user.user_form.cont.fn_text,
		"email_field_title"						: self.dialog_user.user_form.cont.email_text,
		"cell_phone_field_title"				: self.dialog_user.user_form.cont.phone_text,
		"country_field_title"					: self.dialog_user.user_form.cont.country_text,
		"key_words_field_title"					: self.dialog_user.user_form.keywords_text,
		"create_continue_btn"					: self.dialog_user.continue_btn,
		"info_cont_title"						: self.dialog_user.info_btn,
		"group_cont_title"						: self.dialog_user.groups_btn,
		"no_groups_text"						: self.dialog_user.groups_cont.cont.error_text,
		"gen_password_btn"						: self.dialog_user.user_form.generate_password_btn,
		"select_groups_text"					: self.dialog_user.groups_cont.select_group_text,
		"selected_groups_text"					: self.dialog_user.groups_cont.groups_count_text,
		"dialog_create_group_title"				: self.dialog_group.new_group_text,
		"dialog_edit_group_title"				: self.dialog_group.edit_group_text,
		"name_field_title"						: self.dialog_group.group_form.gn_text,
		"no_users_text"							: self.dialog_group.cont.cont.error_text,
		"selected_users_text"					: self.dialog_group.cont.users_count_text,
		"select_users_text"						: self.dialog_group.cont.select_users_text,
		"search_users_text"						: self.dialog_group.cont.search_form.users_search_text,
		"dialog_delete_group_title"				: self.dialog_delete_user_group,
		"dialog_add_to_group_title"				: self.dialog_add_to_group,
		"to_text"								: self.dialog_add_to_group.form_add_to_group.to_title_text,

		"show_on_page_text"						: self.form.obj_per_page_text,

		"cancel_btn_title"						: [
													self.dialog_user.cancel_btn,
													self.dialog_group.cancel_btn,
													self.dialog_add_to_group.form_add_to_group.btn_cancel,
													self.dialog_delete_user_group.btn_delete_no,
													],
		"create_btn_title"						: [
													self.dialog_user.create_btn,
													self.dialog_group.create_btn
													],
		"save_btn_title"						: [
													self.dialog_user.save_btn,
													self.dialog_group.save_btn
													],

		"delete_selected_btn_title"				: [
													self.btn_delete_selected,
													],

		"add_btn_title"							: [

													self.dialog_add_to_group.form_add_to_group.btn_submit,
													],

		"delete_btn_title"						: [
													self.dialog_delete_user_group.btn_delete_yes,
													]

})
localization.render()


from widget_localization_rectangle import LocalizationRectangleWidget
locRectangleWidget = LocalizationRectangleWidget( "user_and_group_manage" )
locRectangleWidget.set_data({
	"top_bar_create_user_btn"		: 	self.btn_create_user,
	"top_bar_delete_selected_btn" 	: 	self.btn_delete_selected,
	"top_bar_add_to_group_btn"		: 	self.btn_add_to_group,
	"top_Bar_create_group_btn"		:	self.btn_create_group,
	"add_to_group_to_title_text"	:	self.dialog_add_to_group.form_add_to_group.to_title_text,

	"continue_btn"					: 	self.dialog_user.continue_btn,
	"selected_users_text"			:	self.dialog_group.cont.users_count_text,
	"selected_groups_text"			:	self.dialog_user.groups_cont.groups_count_text,
	"selected_users_count"			:	self.dialog_group.cont.users_count,
	"selected_groups_count"			:	self.dialog_user.groups_cont.groups_count,

	"objects_per_page_dropdown"		: 	self.form.obj_per_page,


})
locRectangleWidget.render()
