localization_dict = {

	#page titles
	"login_page_title"						: u'Регистрация - ProShare',
	"home_page_title"						: u'Shares - ProShare',
	"smart_folders_page_title"				: u'Smart Folders and Groups - ProShare',
	"smart_contents_page_title"				: u'Съдържание на Smart Folder - ProShare', #smart folder contents page title (private)
	"public_contents_page_title"			: u'Съдържание не Smart Folder - ProShare', #smart folder contents page title (public)
	"macros_page_title"						: u'Макрос - ProShare',
	"edit_macros_page_title"				: u'Редактиране на макрос - ProShare',
	"settings_page_title"					: u'Параметри - ProShare',
	"rules_management_page_title"			: u'Управление на правилата - ProShare',
	"users_groups_management_page_title"	: u'Управление на потребители и групи - ProShare',
	"remote_control_page_title"				: u'Дистанционно управление от ProAdmin - ProShare',
	"proadmin_attention_page_title"			: u'Внимание - ProShare',
	"clear_page_title"						: u'Clear - ProShare', #NEEDED



	#common dialogs and forms strings
	"login" 					: u'Регистрация:',
	"password" 					: u'Парола:',
	"last_name"					: u'Фамилия',
	"first_name"				: u'Име',
	"dialog_add_btn"			: u'Добави',
	"dialog_apply_btn"			: u'Приложи',
	"dialog_cancel_btn" 		: u'Анулирай',
	"dialog_close_btn"			: u'Затвори',
	"dialog_delete_btn"			: u'Изтрий',
	"dialog_download_btn"		: u'Download', #NEEDED
	"dialog_edit_btn"			: u'Редактирай',
	"dialog_ok_btn"				: u'Ok',
	"dialog_save_btn" 			: u'Запиши',
	"dialog_title_confirm"		: u'Потвърди',
	"server"					: u'Сървър:',
	"dialog_upload_btn"			: u'Качи ',
	"email_column_header"		: u'E-mail',
	"error"						: u'Грешка',
	"invalid_data_error_title"	: u'Невалидна дата',
	"check_fields_error"		: u'Проверете полетата',
	"check_name_field_error"	: u'Проверете поле "Име"',
	"btn_delete_selected"		: u"Изтрийте избраното",
	"growl_title_warning"		: u"Предупреждение",
	"growl_title_message"		: u"Съобщение",




	#Errors, messages and warnings
	"unknown_error"								: u"Unknown error occured. Please, try to reload the page or relogin the system. If it repeats, please, contact your administrator.", #NEEDED
	"empty_login_error"							: u"Полето за име не може да бъде празно",
	"empty_name_error"							: u"Полето за регистрация не може да бъде празно",
	"empty_password_error"						: u"Полето за парола не може да бъде празно",
	"invalid_login_or_password_error"			: u"Invalid login or password", #NEEDED
	"files_ignored_warning"						: u"Файловете бяха игнорирани.",
	"nodes_not_exists_warning"					: u"Някои папки и/или файлове бяха изтрити. Моля, заредете страницата отново.",
	"sf_not_exists_warning"						: u"Some Smart Folders or Smart Groups were deleted and no more exist. Please, reload the page.", #NEEDED
	"already_contained_warning"					: u"%s Вече се съдържа %s",
	"subfolders_ignored_warning"				: u"Subfolders were ignored.", #NEEDED
	"folders_added_message"						: u"{0} папката/ките бяха успешно добавени към {1}",
	"nothing_added_message"						: u"Нищо не беше добавено",
	"fields_updated_message"					: u"Fields successfully updated", #NEEDED
	"IllegalCharactersInNameError"				: u"Името не трябва да съдржа, който и да е, от следните символи: *?:\\|/\"&lt&gt",
	"SFAlreadyExistsError"						: u"Smart Smart Folder със същото име вече съществува.",
	"MetaAlreadyExistsError"					: u"Мета поле със същото име вече съществува.",
	"FolderAlreadyContainedError"				: u"Тази папка вече съществува в Smart Folder",
	"AccessDeniedError"							: u"Нямате права да извършите това действие.",
	"SessionExpiredError"						: u"Времето на сесията изтече.",
	"AuthorisationError"						: u"Няма регистриран потребител.",
	"RemoteApplicationDisconnected"				: u"Няма връзка с приложението. ID : %s.",
	"EmptyNameError"							: u"Името е празно.",
	"DirectoryAlreadyExistsError"				: u"Папката вече съществува.",
	"NothingSelectedError"						: u"Не е избрано нищо.",
	"FileAlreadyExistsError"					: u"Дестинацията вече съдържа файл със същото име.",
	"FolderAlreadyExistsError"					: u"Дестинацията вече съдържа папка със същото име.",
	"rules_saved_message"						: u"Rules successfully updated.", #NEEDED
	"rules_inherited_message"					: u"Rules successfully inherited.", #NEEDED
	"inaccessable_rules_warning"				: u"You can't edit rules for this contents:%s", #NEEDED
	"LongNameError"								: u"Name is too long", #NEEDED
	"no_such_directory"							: u"No such directory", #NEEDED
	"fill_all_star_fields_error"				: u'Please, fill all fields marked with a star', #NEEDED
	"file_not_exist"							: u"This file not exist", #NEEDED
	"deleting_no_acces_files_warning"			: u"There are files and folders to which you have no access. These files and folders have not been deleted.", #NEEDED
	"sf_not_exists_error"						: u"Smart Folder does not exist", #NEEDED
	"downloads_not_linked_to_sf"				: u"The downloads are not related to the specified Smart Folder.", #NEEDED
	"folders_and_files_not_found"				: u"Files and folders are not found.", #NEEDED
	"wrong_public_key"							: u"Specified public key is invalid or out of date", #NEEDED
	"downloading_error"							: u"Internal error occurred. Unable to download files and folders.", #NEEDED
	"common_error_message"						: u"An error has occurred. If the error continues, please, contact support of your product provider or your system administrator.",  #NEEDED
	"deleting_no_acces_sfolers_warning"			: u"There are Smart Folders and Groups to which you have no access. These Smart Folders and Groups have not been deleted.",


	#Home
	#top bar buttons
	"btn_upload_files"						: u"Качване на файл",
	"btn_new_folder"						: u"Нова папка",
	"btn_download_selected"					: u"Свалете избраното",
	"btn_edit_selected"						: u"Rename", #NEEDED
	"btn_edit_rights"						: u"Права за редактиране",
	"btn_add_to_smart_folder"				: u"Прибавете към Smart Folder",
	"btn_macros"							: u"Макрос",
	"macro_menu_label"						: u"<p>Run macro</p>", #NEEDED
	"unknown_type"							: u"unknown",
	#contents table
	"contents_tbl_name_title"				: u"Име",
	"contents_tbl_Type_title"				: u"Тип",
	"contents_tbl_Size_title"				: u"Размер",
	"contents_tbl_modified_title"			: u"Променен",
	"contents_tbl_uploaded_title"			: u"Uploaded", #NEEDED
	"node_type_folder"						: u"folder", #NEEDED
	"no_contents_title"						: u"There are no files and folders in this folder", #NEEDED
	#upload dialog
	"dialog_upload_title"					: u"Добави файл",
	"dialog_upload_file_uploader_title"		: u"Файл за качване:",
	"dialog_upload_destination_title"		: u"Дестинация:",
	"dialog_upload_uploader_title"			: u"Select file...", #NEEDED
	#new folder/edit folder dialog
	"dialog_new_folder_title"				: u"Нова папка",
	"dialog_rename_title"					: u"Rename", #NEEDED
	"dialog_folder_name_title"				: u"Име:",
	"dialog_edit_folder_rules_title"		: u"Access rules:", #NEEDED
	#delete selected dialog
	"dialog_delete_selected_title"			: u"Изтрийте избраното",
	#add to Smart Folder dialog
	"dialog_add_to_sf_title"				: u"Добавете към Smart Folder",
	"dialog_dialog_add_to_sf_list_title"	: u"към:",
	"dialog_dialog_add_to_sf_list_new"		: u"Създайте Smart Folder",
	#rules dialog
	"dialog_rules_title"					: u'Edit access rules', #NEEDED
	"inherit_checkbox_title"				: u'apply same rights to contents', #NEEDED
	"processing_rules_in_bg_message"		: u'Access rights will apply in the background. Processing may take a few minutes.', #NEEDED


	#Smart Folders
	"smart_folders_groups_title"		:u"Smart Folders and Groups", #NEEDED
	#top bar buttons
	"btn_new_smart_folder"		: u"Нова папка",
	#delete and edit titles used from page home
	#smart folders table
	"smart_folders_tbl_title"			: u"Smart Folders",
	"smart_folders_tbl_name_title"		: u"Име",
	"smart_folders_tbl_objs_title"		: u"Обекти",
	"smart_folders_tbl_modified_title"	: u"Променен/а",

	"sfg_button_edit"			: u"Edit", #NEEDED
	"sfg_button_add"			: u"Add Smart Folder", #NEEDED
	"sfg_button_delete"			: u"Delete", #NEEDED
	"sfg_button_group"			: u"Group", #NEEDED
	"sfg_button_ungroup"		: u"Ungroup", #NEEDED
	"sfg_button_selectmode"		: u"Select mode", #NEEDED
	"sfg_button_select"			: u"Select", #NEEDED
	"sfg_button_selectall"		: u"Select All", #NEEDED
	"sfg_button_selectnone"		: u"Select None", #NEEDED
	"sfg_button_rules"			: u"Rules", #NEEDED
	"sfg_msg_1"					: u"Please enter name for new folder:", #NEEDED
	"sfg_msg_2"					: u"New Folder", #NEEDED
	"sfg_msg_3"					: u"Folder name is empty", #NEEDED
	"sfg_msg_4"					: u"Not allowed in select mode", #NEEDED
	"sfg_msg_5"					: u"No folder selected", #NEEDED
	"sfg_msg_6"					: u"Please enter new name:", #NEEDED
	"sfg_msg_7"					: u"Please enter name for new group:", #NEEDED
	"sfg_msg_8"					: u"New Group", #NEEDED
	"sfg_msg_9"					: u"Group name is empty", #NEEDED
	"sfg_msg_10"				: u"No items selected", #NEEDED
	"sfg_msg_11"				: u"Group is not specified", #NEEDED


	#Smart Folder contents
	"metafield_type_string"				: u"НИЗ",
	"btn_edit_folders"					: u"Edit folders",  #NEEDED
	"metafield_no_value_title"			: u"Няма стойност",
	"no_files_title"					: u"Няма файлове в тази папка",
	"public_link_btn_title"				: u"Публична връзка",
	"download_all_btn_title"			: u"Download all",   #NEEDED
	#predefined metafields
	"metafield_created"					: u"Създадено",
	"metafield_modified"				: u"Променено",
	"metafield_watchers"				: u"Наблюдатели - да бъдат информирани",
	#add metafield dialog
	"dialog_add_metafield_title"		: u"Добави мета поле",
	"dialog_add_metafield_name_title"	: u"Име:",
	"dialog_add_metafield_type_title"	: u"Тип:",
	"dialog_add_metafield_value_title"	: u"Стойност:",
	#public link dialog
	"dialog_public_link_title"			: u"Публична връзка",
	"dialog_public_link_reset_btn"		: u"Нулиране",
	"dialog_public_clipboard_btn"		: u"Copy to clipboard", #NEEDED
	#add folder dialog
	"dialog_add_folder_title"			: u"Add folder(s)", #NEEDED


	#Macros
	"add_macros_btn"					: u"Добавяне на макрос",
	"import_macros_btn"					: u"Импорт",
	"macros_table_title"				: u"Макрос",
	"macros_table_name_title"			: u"Име",
	"macros_table_event_title"			: u"Събитие",

	#Ecit macros
	"edit_macros_area_caption"				: u"Редактиране на макрос",
	"edit_macros_check_btn"					: u"Проверка",
	"edit_macros_export_btn"				: u"Експорт",
	"edit_macros_name_title"				: u"Име:",
	"edit_macros_event_title"				: u"Събитие:",
	"edit_macros_body_title"				: u"Тяло:",
	"edit_macros_button_macros_checkbox"	: u"Макрос на бутон",
	"edit_macros_on_board_checkbox"			: u"On board", #NEEDED
	"edit_macros_picture_title"				: u"Select picture:", #NEEDED

	#errors
	"fill_all_fields_error"					: u"Fill all fields", #NEEDED
	"vscript_not_compiled_error"			: u"Vscript is not compiled", #NEEDED
	"type_macros_code_error"				: u"Type macros code", #NEEDED
	"fill_macros_fields_error"				: u"Fill macros fields",#NEEDED
	"macro_not_defined_error"				: u"Macro id is not defined", #NEEDED
	"xml_not_correctr_error"				: u"XML is not correct", #NEEDED


	#Design
	#cnt_login
	"greeting"		: u'Здравейте, %s %s',
	"login_error"	: u'Невалидна регистрация или парола',
	#header
	"menu_main_title"			: u'<div style="text-align: center">Дялове</div>',
	"menu_settings_title"		: u'<div style="text-align: center">Параметри</div>',
	"menu_smart_folders_title"	: u'<div style="text-align: center">Smart Folders</div>',
	#add user to group dialog (container_some)
	"find_usr_title"					: u'Намери потребител',
	"find_grp_title"					: u'Намери група',
	"add_usrgrp_diaolg_grp_tab_title"	: u'Добави група',
	"add_usrgrp_diaolg_usr_tab_title"	: u'Добави потребител',

	#Settings
	"settings_proshare_mngmnt_btn"	: u'Управление на дяловете',
	"settings_rules_btn"			: u'Управление на правилата',
	"settings_users_groups_btn"		: u'Управление на потребителите и групите',
	"settings_remote_control_btn"	: u'Дистанционно управление от ProAdmin',


	#Remote scheme (Remote Control)
	"current_scheme_local"		: u'Текуща схема - локално управление на правата',
	"current_scheme_remote"		: u'Текуща схема - Дистанционно управление на правата от ProAdmin',
	##"remote_scheme_page_title"	: u'Remote Control', used "settings_remote_control_btn"
	"radio_btn_local"			: u'Локална схема',
	"radio_btn_remote"			: u'Дистанционна схема',
	#widget_remote_form
	"socket.gaierror" 			: u'Попълнете полето "Сървър"',
	"socket.error" 				: u'Невалиден адрес на сървъра',
	"faultType" 				: u'Проверете полетата "Регистрация" и "Парола"',
	"connection_error"			: u'Грешка при свързването',
	"connection_success"		: u'Успешно свързване. Презаредете страницата и се опитайте да се регистрирате отново.',
	#Proadmin_attention
	"proadmin_attention_text"	: u'Приложението работи по дистанционната схема. Използвайте ProAdmin за конфигуриране на потребители и групи.',
	#Rules Management
	"rules_acl_cancel_btn"		: u'<div class="acl_cancel">Анулиране</div>',
	"rules_acl_apply_btn"		: u'<div class="acl_apply">Прилагане</div>',
	"cont_rules_title"			: u'<div style="padding-left: 15px;" class="acl_container_title">Управление на правата</div>',
	"cont_subjects_title"		: u'<div style="padding-left: 30px;" class="acl_container_title">Потребители и групи</div>',
	"cont_tree_title"			: u'<div class="acl_container_title" style="padding-left: 52px !important;">Обекти</div>',
	#rules_simple
	"widgetuser_rights_name"	: u'Име',
	"widgetuser_rights_access"	: u'Достъп',
	"bttn_apply_to_contents"	: u"Inherit rules", #NEEDED
	"edit_access_rules_title"	: u"Rules Management", #NEEDED
	"btn_back_title"			: u"Back", #NEEDED
	#rights keys (set in proadmin_config)
	"a"							: u'Администриране',
	"w" 						: u'Промяна',
	"r" 						: u'Четене',
	"o"							: u'Edit rights',
	"d"							: u'Изтриване',
	"edit_rights"				: u'Собственик',
	"Full"						: u'Пълни', #title for selecting all available rights options (widget_acl_rules)


	#Users & Groups Management
	##"usr_grp_management_page_title"	: u'Управление на потребители и права', used "settings_users_groups_btn"
	"create_user_btn_text"			: u'Нов потребител',
	"create_group_btn_text"			: u'Нова група',
	"users_tab_title"				: u'Потребители',
	"groups_tab_title"				: u'Групи',
	"fullname_column_header"		: u'Пълно име',
	"groupname_column_header"		: u'Име на група',
	#User dialog
	"dialog_edit_user_title"		: u'Параметри на потребител',
	"info_container_title"			: u'Информация',
	"phone"							: u'Cell Phone',#NEEDED
	"notification_email"			: u'E-mail',#NEEDED
	"country"						: u'Country',#NEEDED
	"key_words"						: u'Key Words',#NEEDED
	#Group dialog
	"dialog_edit_group_title"		: u'Параметри на група',
	"add_usrs_to_grp_btn_title"		: u'Добави потребители',
	"group_name_title"				: u'Име:',
	"add_group"						: u'Добави група',
	"find_user"						: u'Намери потребител',
	"find_group"					: u'Намери група',
	#Delete user or group dialog
	"delete_usr_grp_dialog_title"	: u'Сигурни ли сте, че искате да изтриете избраните обекти',

	"VEE_AddSmartFolder"			:u'Add smart folder',
	"VEE_DeleteSmartFolder"			:u'Delete smart folder',
	"VEE_EditSmartFolder"			:u'Edit smart folder',
	"VEE_AddFileSmartFolder"		:u'Add file to smart folder',
	"VEE_EditFileSmartFolder"		:u'Edit file in smart folder',
	"VEE_DeleteFileSmartFolder"		:u'Delete file from smart folder',
	"VEE_AddFile"					:u'Add file',
	"VEE_EditFile"					:u'Edit file',
	"VEE_DeleteFile"				:u'Delete file',
	"VEE_DownloadFileFromSmartFolder"	: u"Download file from smart folder",
	"VEE_SmartFolderOpenByPulicLink"	: u"Open smart folder by public link",
	"VEE_AddFolder"					:u"Add folder",
	"VEE_EditFolder"				:u"Edit folder",
	"VEE_DeleteFolder"				:u"Delete folder",
	"VEE_AddFolderSmartFolder"		:u"Add folder to smart folder",
	"VEE_EditFolderSmartFolder"		:u"Edit folder in smart folder",
	"VEE_DeleteFolderSmartFolder"	:u"Delete folder from smart folder",


		#log page
	"log_btn_hide_filter"			: u"Скриване филтър",
	"log_btn_show_filter"			: u"Покажи филтър",
	"log_btn_clear_log"				: u"Изчисти",
	"log_btn_refresh_log"			: u"Обнови дневник",
	"log_filter_text"				: u"Филтър настройка",
	"log_by_time"					: u"От времето",
	"log_by_plugin_macros"			: u"От приставката / макроси",
	"log_btn_reset_filter"			: u"Сброс",
	"log_btn_apply_filter"			: u"Нанесете",
	"log_all_messages"				: u"Всички съобщения",
	"log_error"						: u"Грешка",
	"log_invalid_start_date"		: u"Невалидна дата за начало формат",
	"log_invalid_end_date"			: u"Невалидна крайна дата формат",
	"log_invalid_start_end"			: u"Началната дата трябва да бъде по-малко крайна дата",



	#Users & Groups Management
		#page titles
			"users_groups_management_title"	: u'Управление на потребители и групи',

		#top bar buttons
			"create_user_btn_text"			: u'Създаване на потреб.',
			"create_group_btn_text"			: u'Създаване на група',
			"add_selected_to_group_btn_text": u'Добави към група',

		#tableview
			"users_tab_title"				: u'Потребители',
			"groups_tab_title"				: u'Група',

		#datatable header
			"fullname_column_header"		: u'Пълно име',
			"groupname_column_header"		: u'Името на групата',
			"email_column_header"			: u'E-mail',
			"login_column_header"			: u'Влез',
			"group_column_header"			: u'Група',
			"users_count_column_header"		: u'Броят на потребителите',

		#group tab
			"create_new_group_text"			: u'Създаване на нова група',
			"create_new_group_btn"			: u'Създаване',
			"create_new_group_placeholder"	: u'Името на групата',

		#user dialog
			"dialog_create_user_title"		: u'Нов потребител',
			"dialog_edit_user_title"		: u'Редактиране на потребителя',
			"login_field_title"				: u'Влез',
			"password_field_title"			: u'Парола',
			"last_name_field_title"			: u'Фамилно име',
			"first_name_field_title"		: u'Име',
			"email_field_title"				: u'E-mail',
			"cell_phone_field_title"		: u'Телефонен номер',
			"country_field_title"			: u'Страна',
			"key_words_field_title"			: u'Ключови думи',
			"create_continue_btn"			: u'Създаване и продълж.',
			"info_cont_title"				: u'Информация',
			"group_cont_title"				: u'Група',
			"add_groups_btn"				: u'Добавяне на група',
			"no_groups_text"				: u'Наличните няма групи',
			"gen_password_btn"				: u'Генериране на парола',
			"send_email_checkbox"			: u'Изпрати имейл на потребителя',
			"select_groups_text"			: u'Изберете групите:',
			"selected_groups_text"			: u'Брой на избраните групи:',

		#group dialog
			"dialog_create_group_title"		: u'Новата група',
			"dialog_edit_group_title"		: u'Редактиране на група',
			"name_field_title"				: u'Име',
			"add_users_btn"					: u'Добавяне на потребител.',
			"no_users_text"					: u'Не регистрирани потребители',
			"selected_users_text"			: u"Брой на избрани потребители:",
			"select_users_text"				: u'Изберете потребители:',
			"search_users_text"				: u'Ръководство на филтър',

		#add user/group dialog
			"dialog_add_user_title"			: u"Търсене на потребители",
			"dialog_add_group_title"		: u"Търсене на група",
			"search_doesnt_find"			: u"За съжаление не е намерен",
			"search_field_title_user"		: u"Въведете име, фамилия или Е-мейл",
			"search_field_title_group"		: u"Въведете името на групата",

		#delete dialog
			"dialog_delete_user_title"		: u'Махни обекти',
			"dialog_delete_group_title"		: u'Махни обекти',

		#dialog add users to group
			"dialog_add_to_group_title"		: u'Добави към група',
			"to_text"						: u'в',
			"create_new_group_text"			: u'Създаване на нова група',

		"cancel_btn_title"					: u'Отменяне',
		"create_btn_title"					: u'Създаване',
		"save_btn_title"					: u'Спасяване',
		"delete_selected_btn_title"			: u'Изтриване на избраните',
		"add_btn_title"						: u'Добави',
		"delete_btn_title"					: u'Премахнете',
		"dd_all_users"						: u'Всички потребители',
		"show_on_page_text"					: u'Покажи по',


		#remote_setting_page
		"settings_remote_page_title" 		: u'Set scheme',
		"text_current_scheme"				: u'Current scheme',
		"radio_btn_local"					: u'Local scheme',
		"radio_btn_remote"					: u'Remote scheme',
		"host"								: u'Host:',
		"apply_btn"							: u'Apply',
		"test_btn"							: u'Test connection',
		"use_settings_btn"					: u'Use this settings',
		"refresh_btn"						: u'Refresh',
		"last_sync_text"					: u'Last sync: ',
		"syns_state_text"					: u'Sync thread status: ',
		"object_text"						: u'Objects: ',
		"user_text"							: u'Users: ',
		"connect_ip_success"				: u'Connect to ',
		"connect_ip_fail"					: u'Connection to IP address failed',
		"open_session_success"				: u'Open session ',
		"open_session_fail"					: u'Opening session failed: incorrect login or password',
		"proadmin_connection_fail"			: u'Connection to ProAdmin failed: there is no app on selected IP or login and password are incorrect',
		"at"								: u' at ',
		"test_sso_btn"						: u'Test SSO',
		"cancel_btn"						: u'Cancel',
		"close_btn"							: u'Close',
		"warning_test_sso"					: u"You'll be redirected to ProAdmin. If something wrong press back button in your browser.",
		"success_sso"						: u'SSO works.',

		#errors
		"fill_all_fields_error"					: u"Fill all fields",
		"vscript_not_compiled_error"			: u"Vscript is not compiled",
		"type_macros_code_error"				: u"Type macros code",
		"fill_macros_fields_error"				: u"Fill macros fields",
		"macro_not_defined_error"				: u"Macro id is not defined",
		"xml_not_correctr_error"				: u"XML is not correct",

		#errors
			"warning_title"					: u'Внимание!',
			"error_title"					: u'Дървеница!',
			"select_objects_error"			: u'Преминете към',
			"fill_group_name_field"			: u'Посочете името на групата',
			"group_name_already_exists"		: u'Група с това име вече съществува',
			"group_doesnt_exist"			: u'Групата не съществува',
			"fill_all_fields_with_star_error" : u'Моля попълнете всички полета',
			"user_doesnt_exist_error"		: u'Потребителят не съществува. Обновяване на страницата.',
			"group_doesnt_exist_error"		: u'Групата не съществува. Обновяване на страницата.',
			"user_login_already_exist_error": u'Това потребителско име вече съществува',
			"user_email_is_incorrect_error" : u'Невалиден имейл адрес',
			"user_phone_illegal_characters"	: u'Телефонният номер е невалиден',
			"user_password_is_empty_error"	: u'Въведете паролата',



	############################################################################
	"license" : u"""Ce logiciel et sa documentation sont la propriete de VDOM Box International. Il est interdit de les traduire, decompiler, modifier, adapter et corriger. Il vous est interdit de supprimer ou modifier les informations de licence et de le transmettre a des tiers. La location et le pret du logiciel sont interdits. Vous ne pouvez pas utiliser ce logiciel sur un autre materiel que celui fournie avec celui-ci. Seul l’auteur est habilite a effectuer ces operations.
Si vous effectuez une des operations ci-dessus, vos droits d’utilisation sont automatiquement resilies et l’auteur pourra recourir en justice.
Vous etes autorise, a posseder a des fins de sauvegarde uniquement des copies du fichier XML representant l’application sur d’autres supports de stockage que ceux inclus dans le materiel executant l’application. Vous n’etes pas autorise a faire de copies de la documentation papier.
Vous n’etes autorise a installer et utiliser le logiciel que sur un seul materiel executant le serveur d’application VDOM (generalement une VDOM Box). La licence de ce logiciel est associe a un identifiant unique d’utilisateur stocke sur la carte a Puce equipant la VDOM Box, vous n’etes pas autorise a utiliser la licence de ce logiciel pour un autre utilisateur possedant un identifiant unique different.
Transfert de licence. Pour transferer la licence de ce logiciel sur un autre utilisateur unique, celle-ci doit d’abord etre supprime de la carte a puce autorisant du precedent utilisateur, ce transfert ne peut se faire que par le distributeur de cette licence.
En utilisant ce logiciel, vous vous engagez a respecter les droits d’auteur, et a veiller a ce que les autres utilisateurs les respectent eux-memes.
Ce logiciel est protege en France par les lois sur la propriete intellectuelle ainsi qu’a l’etranger par les conventions internationales sur le droit d’auteur (convention de Berne).
La violation de l'un des droits de l'auteur du logiciel est un delit de contrefacon sanctionnee en France par l'article L335-2 du code de la propriete intellectuelle.
Le logiciel est fourni tel quel, sans aucune garantie. L'auteur ne saurait voir sa responsabilite engagee en cas de dommages de quelque nature que ce soit subis par l'utilisateur ou des tiers et resultant directement ou indirectement de son utilisation, notamment la perte de donnees, ou toute perte financiere resultant de son utilisation ou de l’impossibilite de l’utiliser, et ceci meme si l’auteur a ete prevenu de la possibilite de tels dommages. En tout etat de cause, la responsabilite de l’auteur ne pourra exceder le montant paye pour l’acquisition de la licence.
Si le logiciel propose est presente comme etant une mise a jour, vous devez etre deja titulaire d’une licence anterieure du meme logiciel pour pouvoir en beneficier. Une mise a jour complete ou remplace la licence et la version anterieure du logiciel. La mise a jour et la licence originale doivent etre considerees comme un produit unique. Vous n’etes donc pas autorise a les ceder ou donner separement.""",

	"license_button" : u"License",

	#license page
	"agree_button"				: u'Agree',
	"disagree_button"			: u'Disagree',
	"close_button"				: u'Close',
	"disagree_warning"			: u'You have to agree with license to use product',
	"select_operation_mode"		: u'Select the application operating mode:',
	"standalone_mode"			: u'Standalone',
	"proadmin_mode"				: u'ProAdmin connection',
	"proadmin_page_warning"		: u'You can set up ProAdmin connection on special page.',
	"go_button"					: u'Go',
	"password_title"			: u'Set password for administrator account:',
	"password_field"			: u'Password:',
	"confirm_password_field"	: u'Confirm password:',
	"apply_password"			: u'Apply',

	#proadmin_v2
	"system_login_title"			: u'System login',
	"system_account"				: u'System account:',
	"login_btn"						: u'Login',
	"users_container_label"			: u'Users',
	"incorrect_login"				:u'Incorrect login or password',
	"no_vdom"						:u'There is no VDOM',
	"standalone"					:u'Standalone',
	"proadmin_connection"			:u'ProAdmin connection',
	"restart_connectoin_btn"		:u'Restart connection',
	"reset_btn"						:u'Reset',
	"greating_title"				:u'Logged in ProSuite as %s',
	"account_column"				:u'Login',
	"name_column"					:u'Name',
	"login_column"					:u'Login as',
	"standalone_text"				:u'What is standalone connection?',
	"proadmin_text"					:u'What is ProAdmin connection?',
	"logout_hint"					:u'click to log out from ProSuite',
	"user_not_logged_in"			:u'Not logged in...',
	"proadmin_management"			:u'ProAdmin management',
	"user_management"				:u'Users management',

	#log off/start button
	"switch_to"						: u"Switch to",
	"logout"						: u"Log Out",
	"logoff_caption"				: u"You have been logged off",
	"logoff_message"				: u"You will be redirected to the login page in few seconds",

	#free_space
	"Gb"			:u'Gb',
	"Mb"			:u'Mb',
	"of"			:u' of ',
	"free"			:u' free',
}

lang_rectangle = {
	#'id' 							: 	[ 	left,		top,	width,	height 	]
	"user_and_group_manage"	: {
		#top bar
			"top_bar_create_user_btn"		: 	[	"18", 	"85", 	"105", 	"35" 	],
			"top_bar_delete_selected_btn" 	: 	[ 	"133", 	"85", 	"120", 	"35" 	],
			"top_bar_add_to_group_btn"		: 	[ 	"263", 	"85", 	"88", 	"35" 	],
			"top_Bar_create_group_btn"		:	[	"18",	"85",	"103",	"35"	],

		#add to group dialog
			"add_to_group_to_title_text"	:	[ 	"17",	"155",	"15",	"14"	],

		#add user group dialog
			"add_ug_cancel_btn"				:	[	"218",	"397",	"80",	"33"	],
			"add_ug_add_btn"				:	[	"310",	"397",	"80",	"33"	],

		#create user dialog
			"continue_btn"					:	[	"111",	"582",	"188",	"25"	],
			"add_groups_btn"				:	[	"14",	"27",	"140",	"32"	],
			"del_sel_groups_btn"			:	[	"160",	"27",	"190",	"32"	],

		#create group dialog
			"add_users_btn"					:	[	"17",	"67",	"200",	"32"	],
			"del_sel_users_btn"				:	[	"218",	"67",	"190",	"32"	],
			"selected_users_text"			:	[	"19",	"364",	"180",	"14"	],
			"selected_groups_text"			:	[	"8",	"446",	"155",	"14"	],
			"selected_users_count"			:	[	"205",	"364",	"50",	"14"	],
			"selected_groups_count"			:	[	"170",	"446",	"50",	"14"	],

			"objects_per_page_dropdown"		: 	[	"75",	"1",	"52",	"22"	],

		}
}


