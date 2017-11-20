localization_dict = {

	#page titles
	"login_page_title"						: u'Login - ProShare',
	"home_page_title"						: u'Fichiers - ProShare',
	"smart_folders_page_title"				: u'Gestion des dossiers intelligents - ProShare',
	"smart_contents_page_title"				: u'Contenu des Dossiers intelligents - ProShare', #smart folder contents page title (private)
	"public_contents_page_title"			: u'Contenu des Dossiers intelligents - ProShare', #smart folder contents page title (public)
	"macros_page_title"						: u'Macros - ProShare',
	"edit_macros_page_title"				: u'Editer les macros - ProShare',
	"settings_page_title"					: u'Paramètres - ProShare',
	"rules_management_page_title"			: u'Gestion des règles - ProShare',
	"users_groups_management_page_title"	: u'Utilisateurs & Groupes - ProShare',
	"remote_control_page_title"				: u'Contrôler par ProAdmin - ProShare',
	"proadmin_attention_page_title"			: u'Attention - ProShare',
	"clear_page_title"						: u'Effacé - ProShare',



	#common dialogs and forms strings
	"login" 					: u'Utilisateur :',
	"password" 					: u'Mot de passe :',
	"last_name"					: u'Nom de famille',
	"first_name"				: u'Prénom',
	"dialog_add_btn"			: u'Ajouter',
	"dialog_apply_btn"			: u'Appliquer',
	"dialog_cancel_btn" 		: u'Annuler',
	"dialog_close_btn"			: u'Fermer',
	"dialog_delete_btn"			: u'Supprimer',
	"dialog_download_btn"		: u'Téléchargement',
	"dialog_edit_btn"			: u'Editer',
	"dialog_ok_btn"				: u'Ok',
	"dialog_save_btn" 			: u'Enregistrer',
	"dialog_title_confirm"		: u'Confirmer',
	"server"					: u'Serveur :',
	"dialog_upload_btn"			: u'Télécharger',
	"email_column_header"		: u'E-mail',
	"error"						: u'Erreur',
	"invalid_data_error_title"	: u'Date invalide',
	"check_fields_error"		: u'Vérifier les champs',
	"check_name_field_error"	: u'Vérifier le champ "Nom"',
	"btn_delete_selected"		: u"Supprimer la sélection",
	"growl_title_warning"		: u"Attention",
	"growl_title_message"		: u"Message",




	#Errors, messages and warnings
	"unknown_error"								: u"Unknown error occured. Please, try to reload the page or relogin the system. If it repeats, please, contact your administrator.",
	"empty_name_error"							: u"Entrez le nom.",
	"empty_login_error"							: u"Remplissez le champ login.",
	"empty_password_error"						: u"Le mot de passe ne peut pas être vide.",
	"invalid_login_or_password_error"			: u"Mot de passe ou login incorrect",
	"files_ignored_warning"						: u"Les fichiers ont été ignorés.",
	"nodes_not_exists_warning"					: u"Certains des fichiers ou répertoires n'existent plus, veuiller recharger la page.",
	"sf_not_exists_warning"						: u"Certains des dossiers intelligents où groupes de dossiers ont été supprimé, veuillez recharger la page.",
	"already_contained_warning"					: u"%s se trouve déjà dans %s",
	"subfolders_ignored_warning"				: u"Sous-répertoires ignorés.",
	"folders_added_message"						: u"{0} répertoire(s) ont été ajoutés avec succès dans {1}",
	"nothing_added_message"						: u"Rien n'a été ajouté",
	"fields_updated_message"					: u"Champs mis à jour avec succès",
	"IllegalCharactersInNameError"				: u"Un nom ne peut contenir l`un de ces caratères: *?:\\|/\"&lt&gt",
	"SFAlreadyExistsError"						: u"Un dossier intelligent avec le même nom existe déjà.",
	"MetaAlreadyExistsError"					: u"Un champ de méta données existe déjà avec le même nom.",
	"FolderAlreadyContainedError"				: u"Ce répertoire existe déjà dans le Dossier Intelligent.",
	"AccessDeniedError"							: u"Vous n'avez pas les droits nécessaires pour effectuer cette action.",
	"SessionExpiredError"						: u"La session a expiré.",
	"AuthorisationError"						: u"Aucun utilisateur n'est connecté.",
	"RemoteApplicationDisconnected"				: u"Application déconnectée. ID : %s.",
	"EmptyNameError"							: u"le champ du nom est vide.",
	"DirectoryAlreadyExistsError"				: u"Le répertoire existe déjà.",
	"NothingSelectedError"						: u"La sélection courante est vide.",
	"FileAlreadyExistsError"					: u"La destination contient déjà des fichiers avec le même nom.",
	"FolderAlreadyExistsError"					: u"La destination contient déjà des répertoires avec le même nom.",
	"rules_saved_message"						: u"Droits mis à jour avec succès.",
	"rules_inherited_message"					: u"Droits hérités avec succès.",
	"inaccessable_rules_warning"				: u"Vous ne pouvez pas modifier les droits pour ce contenu:%s",
	"LongNameError"								: u"Nom trop long",
	"no_such_directory"							: u"Répertoire invalide",
	"fill_all_star_fields_error"				: u"Remplissez tous les champs marqués d'un astérisque.",
	"phone_illegal_characters"					: u"Le numéro de téléphone contient des caractères incorrects.",
	"file_not_exist"							: u"Ce fichier n'existe plus.",
	"deleting_no_acces_files_warning"			: u"Vous n'avez pas les droits suffisants sur certains des fichiers que vous tentez de supprimer, il ne le seront donc pas.",
	"sf_not_exists_error"						: u"Le dossier intelligent n'existe pas.",
	"downloads_not_linked_to_sf"				: u"Vous tentez de télécharger un fichier qui ne se trouve pas dans ce dossier intelligent.",
	"folders_and_files_not_found"				: u"Les fichiers ou les répertoires n'ont pas pu être trouvé.",
	"wrong_public_key"							: u"La clef public de ce dossier intelligent n'est pas valide ou périmée.",
	"downloading_error"							: u"Une erreur interne s'est produite, vous ne pouvez pas télécharger ce fichier ou répertoire.",
	"common_error_message"						: u"Une erreur est survenue, si elle se reproduit, veuillez contacter le support pour la signaler.",
	"deleting_no_acces_sfolers_warning"			: u"There are Smart Folders and Groups to which you have no access. These Smart Folders and Groups have not been deleted.",





	#Home
	#top bar buttons
	"btn_upload_files"			: u"Télécharger",
	"btn_new_folder"			: u"Nouveau dossier",
	"btn_download_selected"		: u"Télécharger la sélection",
	"btn_edit_selected"			: u"Renommer",
	"btn_edit_rights"			: u"Editer les droits",
	"btn_add_to_smart_folder"	: u"Ajouter aux dossiers intelligents",
	"btn_macros"				: u"Macros",
	"macro_menu_label"			: u"<p>Plugin</p>",
	#contents table
	"contents_tbl_name_title"		: u"Nom",
	"contents_tbl_Type_title"		: u"Type",
	"contents_tbl_Size_title"		: u"Taille",
	"contents_tbl_modified_title"	: u"Modifié le",
	"contents_tbl_uploaded_title"	: u"Chargé",
	"node_type_folder"				: u"Dossier",
	"no_contents_title"				: u"Pas de fichiers ou dossiers dans ce dossier",
	"unknown_type"					: u"unknown",
	#upload dialog
	"dialog_upload_title"					: u"Ajouter un fichier",
	"dialog_upload_file_uploader_title"		: u"Fichier à télécharger :",
	"dialog_upload_destination_title"		: u"Destination :",
	"dialog_upload_uploader_title"			: u"Choisir le fichier...",
	#new folder/edit folder dialog
	"dialog_new_folder_title"			: u"Nouveau dossier",
	"dialog_rename_title"				: u"Renommer",
	"dialog_folder_name_title"			: u"Nom :",
	"dialog_edit_folder_rules_title"	: u"Règles d'accès :",
	#delete selected dialog
	"dialog_delete_selected_title"		: u"Supprimer la sélection",
	#add to Smart Folder dialog
	"dialog_add_to_sf_title"				: u"Ajouter aux dossiers intelligents",
	"dialog_dialog_add_to_sf_list_title"	: u"Vers :",
	"dialog_dialog_add_to_sf_list_new"		: u"Créer un nouveau",
	#rules dialog
	"dialog_rules_title"					: u'Editer la gestion des accès',
	"inherit_checkbox_title"				: u'Appliquer les mêmes droits aux contenus',
	"processing_rules_in_bg_message"		: u'La gestion des droits se font en tâche de fond, ce processus peut prendre quelques minutes',



	#Smart Folders
	"smart_folders_groups_title"		:u"Gestion des dossiers intelligents",
	#top bar buttons
	"btn_new_smart_folder"		: u"Nouveau dossier",
	#delete and edit titles used from page home
	#smart folders table
	"smart_folders_tbl_title"			: u"Dossiers Intelligents",
	"smart_folders_tbl_name_title"		: u"Nom",
	"smart_folders_tbl_objs_title"		: u"Objets",
	"smart_folders_tbl_modified_title"	: u"Modifié le",

	"sfg_button_edit"			: u"Editer",
	"sfg_button_add"			: u"Ajouter un dossier intelligent",
	"sfg_button_delete"			: u"Supprimer",
	"sfg_button_group"			: u"Grouper",
	"sfg_button_ungroup"		: u"Dégrouper",
	"sfg_button_selectmode"		: u"Mode : Sélection",
	"sfg_button_select"			: u"Sélection",
	"sfg_button_selectall"		: u"Tous",
	"sfg_button_selectnone"		: u"Aucun",
	"sfg_button_rules"			: u"Droits",
	"sfg_msg_1"					: u"Veuillez saisir le nom du nouveau fichier :",
	"sfg_msg_2"					: u"Nouveau fichier",
	"sfg_msg_3"					: u"Le nom du fichier est vide",
	"sfg_msg_4"					: u"Cette opération n'est pas permiser dans le mode sélection.",
	"sfg_msg_5"					: u"Aucun répertoire n'a été sélectionné",
	"sfg_msg_6"					: u"Veuillez saisir un nouveau nom :",
	"sfg_msg_7"					: u"Veuillez saisir un nouveau nom pour le groupe :",
	"sfg_msg_8"					: u"Nouveau groupe",
	"sfg_msg_9"					: u"Le nom du groupe est vide",
	"sfg_msg_10"				: u"Aucun élément sélectionné.",
	"sfg_msg_11"				: u"Aucun groupe spécifié.",

	#Smart Folder contents
	"metafield_type_string"				: u"CHAINE",
	"btn_edit_folders"					: u"Editer",
	"metafield_no_value_title"			: u"Aucune valeur",
	"no_files_title"					: u"Il n'y a aucun fichier dans ce répertoire",
	"public_link_btn_title"				: u"Lien public",
	"download_all_btn_title"			: u"Tout télécharger",

	#predefined metafields
	"metafield_created"					: u"Créé",
	"metafield_modified"				: u"Modifié",
	"metafield_watchers"				: u"Notification",
	#add metafield dialog
	"dialog_add_metafield_title"		: u"Ajout de métadonnées",
	"dialog_add_metafield_name_title"	: u"Nom :",
	"dialog_add_metafield_type_title"	: u"Type :",
	"dialog_add_metafield_value_title"	: u"Valeur :",
	#public link dialog
	"dialog_public_link_title"			: u"Lien public",
	"dialog_public_link_reset_btn"		: u"RAZ",
	"dialog_public_clipboard_btn"		: u"Copier dans presse papier",
	#add folder dialog
	"dialog_add_folder_title"			: u"Ajouter un champ(s)",



	#Macros
	"add_macros_btn"					: u"Ajouter une macro",
	"import_macros_btn"					: u"Importer",
	"macros_table_title"				: u"Macros",
	"macros_table_name_title"			: u"Nom",
	"macros_table_event_title"			: u"Evènement",

	#Ecit macros
	"edit_macros_area_caption"				: u"Editer une macro",
	"edit_macros_check_btn"					: u"Vérifier",
	"edit_macros_export_btn"				: u"Exporter",
	"edit_macros_name_title"				: u"Nom :",
	"edit_macros_event_title"				: u"Evènement :",
	"edit_macros_body_title"				: u"Corps :",
	"edit_macros_button_macros_checkbox"	: u"Bouton macro",
	"edit_macros_on_board_checkbox"			: u"Dans le menu",
	"edit_macros_picture_title"				: u"Sélectionner une image :",

	#errors
	"fill_all_fields_error"					: u"Remplissez tous les champs.",
	"vscript_not_compiled_error"			: u"VScript non complilé",
	"type_macros_code_error"				: u"Votre macro ne contient aucun code.",
	"fill_macros_fields_error"				: u"Remplissez les champs de la macro.",
	"macro_not_defined_error"				: u"L'identifiant de la macro n'existe pas.",
	"xml_not_correctr_error"				: u"Le source XML de votre plugin est incorrect.",

	#Design
	#cnt_login
	"greeting"		: u'Bonjour, %s %s',
	"login_error"	: u'Mot de passe ou login incorrect',
	#header
	"menu_main_title"			: u'<div style="text-align: center">Fichiers</div>',
	"menu_settings_title"		: u'<div style="text-align: center">Paramètres</div>',
	"menu_smart_folders_title"	: u'<div style="text-align: center">Dossiers Intelligents</div>',
	#add user to group dialog (container_some)
	"find_usr_title"					: u'Trouver un utilisateur',
	"find_grp_title"					: u'Trouver un groupe',
	"add_usrgrp_diaolg_grp_tab_title"	: u'Ajouter un groupe',
	"add_usrgrp_diaolg_usr_tab_title"	: u'Ajouter un utilisateur',

	#Settings 												"settings_proshare_mngmnt_btn"	: u'Gestion des partages',
	"settings_rules_btn"			: u'Gestion des règles',
	"settings_users_groups_btn"		: u'Utilisateurs & Groupes',
	"settings_remote_control_btn"	: u'Gestion des droits',


	#Remote scheme (Remote Control)
	"current_scheme_local"		: u'Méthode active : Local',
	"current_scheme_remote"		: u'Méthode active : ProAdmin',
	##"remote_scheme_page_title"	: u'Remote Control', used "settings_remote_control_btn"
	"radio_btn_local"			: u'Gestion locale',
	"radio_btn_remote"			: u'Gestion via ProAdmin',
	#widget_remote_form
	"socket.gaierror" 			: u'Veuiller renseigner le champ "Serveur"',
	"socket.error" 				: u'Adresse du serveur incorrecte',
	"faultType" 				: u'Vérifiez les champs "Login" et "Mot de passe".',
	"connection_error"			: u'Erreur de connexion',
	"connection_success"		: u'Connexion réussie. Recharger la page et essayer de vous identifier à nouveau.',


	#Proadmin_attention
	"proadmin_attention_text"	: u"L'application est gérée par ProAdmin, veuillez utiliser ce logiciel pour configurer les utilisateurs et les groupes.",


	#Rules Management
	"rules_acl_cancel_btn"		: u'<div class="acl_cancel">Annuler</div>',
	"rules_acl_apply_btn"		: u'<div class="acl_apply">Appliquer</div>',
	"cont_rules_title"			: u'<div style="padding-left: 15px;" class="acl_container_title">Gestion des droits</div>',
	"cont_subjects_title"		: u'<div style="padding-left: 30px;" class="acl_container_title">Utilisateurs et groupes</div>',
	"cont_tree_title"			: u'<div class="acl_container_title" style="padding-left: 52px !important;">Objets</div>',
	#rules_simple
	"widgetuser_rights_name"	: u'Nom',
	"widgetuser_rights_access"	: u'Accès',
	"bttn_apply_to_contents"	: u"Héritage des droits",
	"edit_access_rules_title"	: u"Gestion des règles",
	"btn_back_title"			: u"Retour",
	#rights keys (set in proadmin_config)
	"a"							: u'Administration',
	"w" 						: u'Modification',
	"r" 						: u'Lecture',
	"o"							: u'Editer les droits',
	"d"							: u'Suppression',
	"edit_rights"				: u'Propriétaire',
	"Full"						: u'Tous', #title for selecting all available rights options (widget_acl_rules)


	#Users & Groups Management
	"usr_grp_management_page_title"	: u'Gestion des utlisateurs et des groupes',
	"create_user_btn_text"			: u'Créer un utilisateur',
	"create_group_btn_text"			: u'Créer un groupe',
	"users_tab_title"				: u'Utilisateurs',
	"groups_tab_title"				: u'Groupes',
	"fullname_column_header"		: u'Nom et prénom',
	"groupname_column_header"		: u'Nom du groupe',

	#User dialog
	"dialog_edit_user_title"		: u"Modifier l'utilisateur",
	"info_container_title"			: u'Informations',
	"phone"							: u'Tel. Portable',#NEEDED
	"notification_email"			: u'E-mail',#NEEDED
	"country"						: u'Pays',#NEEDED
	"key_words"						: u'Mots clefs',#NEEDED
	#Group dialog
	"dialog_edit_group_title"		: u'Modifier le groupe',
	"add_usrs_to_grp_btn_title"		: u'Ajouter des utilisateurs',
	"group_name_title"				: u'Nom :',
	"add_group"						: u'Ajouter un groupe',
	"find_user"						: u'Trouver un utilisateur',
	"find_group"					: u'Trouver un groupe',
	#Delete user or group dialog
	"delete_usr_grp_dialog_title"	: u'Supprimer un utilisateur ou un groupe ?',


	"VEE_AddSmartFolder"			:u"Ajout d'un dossier intelligent",
	"VEE_DeleteSmartFolder"			:u"Suppression d'un dossier intelligent",
	"VEE_EditSmartFolder"			:u"Edition d'un dossier intelligent",
	"VEE_AddFileSmartFolder"		:u"Ajout d'un fichier à un dossier intelligent",
	"VEE_EditFileSmartFolder"		:u"Editer un fichier dans un dossier intelligent",
	"VEE_DeleteFileSmartFolder"		:u"Suppression d'un fichier dans un dossier intelligent",
	"VEE_AddFile"					:u"Ajout d'un fichier",
	"VEE_EditFile"					:u"Edition d'un fichier",
	"VEE_DeleteFile"				:u"Suppression d'un fichier",
	"VEE_DownloadFileFromSmartFolder"	: u"Téléchargement d'un fichier depuis un dossier intelligent",
	"VEE_SmartFolderOpenByPulicLink"	: u"Ouverture d'un dossier intelligent depuis un lien public",
	"VEE_AddFolder"					:u"Ajout d'un répertoire",
	"VEE_EditFolder"				:u"Edition d'un répertoire",
	"VEE_DeleteFolder"				:u"Suppression d'un répertoire",
	"VEE_AddFolderSmartFolder"		:u"Ajout d'un répertorie à un dossier intelligent",
	"VEE_EditFolderSmartFolder"		:u"Edition d'un répertoire dans un dossier intelligent",
	"VEE_DeleteFolderSmartFolder"	:u"Suppression d'un répertoire depuis un dossier intelliegent",


	#log page
	"log_btn_hide_filter"			: u"Masquer filtre",
	"log_btn_show_filter"			: u"Afficher filtre",
	"log_btn_clear_log"				: u"Effacer",
	"log_btn_refresh_log"			: u"Actualiser journal",
	"log_filter_text"				: u"Filtre de configuration",
	"log_by_time"					: u"En temps",
	"log_by_plugin_macros"			: u"En plugin / macros",
	"log_btn_reset_filter"			: u"Reset",
	"log_btn_apply_filter"			: u"Appliquer",
	"log_all_messages"				: u"Tous les messages",
	"log_error"						: u"Erreur",
	"log_invalid_start_date"		: u"Invalid date de début",
	"log_invalid_end_date"			: u"Date de fin incorrecte",
	"log_invalid_start_end"			: u"Date de début doit être inférieure à la date de fin",


	#Users & Groups Management
		#page titles
			"users_groups_management_title"	: u'Gestion des utilisateurs et des groupes',

		#top bar buttons
			"create_user_btn_text"			: u'Créer un utilisateur',
			"create_group_btn_text"			: u'Créer un groupe',
			"add_selected_to_group_btn_text": u'Ajouter au groupe',

		#tableview
			"users_tab_title"				: u'Utilisateurs',
			"groups_tab_title"				: u'Groupes',

		#datatable header
			"fullname_column_header"		: u'Nom et prénom',
			"groupname_column_header"		: u'Nom du groupe',
			"email_column_header"			: u'E-mail',
			"login_column_header"			: u'Login',
			"group_column_header"			: u'Groupe',
			"users_count_column_header"		: u"Le nombre d'utilisateurs",

		#group tab
			"create_new_group_text"			: u'Créer un nouveau groupe',
			"create_new_group_btn"			: u'Créer',
			"create_new_group_placeholder"	: u'Nom du groupe',

		#user dialog
			"dialog_create_user_title"		: u'Nouvel utilisateur',
			"dialog_edit_user_title"		: u"Modifier l'utilisateur",
			"login_field_title"				: u'Login',
			"password_field_title"			: u'Mot de passe',
			"last_name_field_title"			: u'Nom de famille',
			"first_name_field_title"		: u'Prénom',
			"email_field_title"				: u'E-mail',
			"cell_phone_field_title"		: u'Téléphone',
			"country_field_title"			: u'Pays',
			"key_words_field_title"			: u'Mots clés',
			"create_continue_btn"			: u'Créer et continuer',
			"info_cont_title"				: u'Informations',
			"group_cont_title"				: u'Groupes',
			"add_groups_btn"				: u'Ajouter un groupe',
			"no_groups_text"				: u"Pas de groupes disponibles",
			"gen_password_btn"				: u'Générer mot de passe',
			"send_email_checkbox"			: u"Envoyer un e-mail à l'utilisateur",
			"select_groups_text"			: u'Sélectionnez les groupes :',
			"selected_groups_text"			: u'Plusieurs groupes choisis :',

		#group dialog
			"dialog_create_group_title"		: u'Nouveau groupe',
			"dialog_edit_group_title"		: u'Modifier le groupe',
			"name_field_title"				: u'Nom',
			"add_users_btn"					: u'Ajouter un utilisateur',
			"no_users_text"					: u"Il n'y a pas les utilisateurs enregistrés",
			"selected_users_text"			: u"Nombre d'utilisateurs sélectionnés :",
			"select_users_text"				: u'Sélectionnez les utilisateurs :',
			"search_users_text"				: u'Filtre utilisateur',

		#add user/group dialog
			"dialog_add_user_title"			: u'Rechercher des utilisateurs',
			"dialog_add_group_title"		: u'Rechercher des groupes',
			"search_doesnt_find"			: u'Votre recherche ne correspond à',
			"search_field_title_user"		: u'Entrez le nom, prénom ou adresse e-mail',
			"search_field_title_group"		: u'Entrez le nom du groupe',

		#delete dialog
			"dialog_delete_user_title"		: u'Enlevez les objets',
			"dialog_delete_group_title"		: u'Enlevez les objets',

		#dialog add users to group
			"dialog_add_to_group_title"		: u'Ajouter au groupe',
			"to_text"						: u'à',
			"create_new_group_text"			: u'Créer un nouveau groupe',

		"cancel_btn_title"					: u'Annuler',
		"create_btn_title"					: u'Créer',
		"save_btn_title"					: u'Sauver',
		"delete_selected_btn_title"			: u'Supprimer la sélection',
		"add_btn_title"						: u'Ajouter',
		"delete_btn_title"					: u'Effacer',
		"dd_all_users"						: u'Tous les utilisateurs',
		"show_on_page_text"					: u'Afficher par',


		#remote_setting_page
		"settings_remote_page_title" 		: u'Sélectionnez une méthode',
		"text_current_scheme"				: u'Méthode active',
		"radio_btn_local"					: u'Gestion locale',
		"radio_btn_remote"					: u'Gestion par ProAdmin',
		"host"								: u'Hôte :',
		"apply_btn"							: u'Appliquer',
		"test_btn"							: u'Tester la connection',
		"use_settings_btn"					: u'Activer',
		"refresh_btn"						: u'Rafrechir',
		"last_sync_text"					: u'Dernière sync. :',
		"syns_state_text"					: u'Statut de la sync. :',
		"object_text"						: u'Objets :',
		"user_text"							: u'Utilisateurs :',
		"connect_ip_success"				: u'Connecté à',
		"connect_ip_fail"					: u"La connexion à l'adresse IP a échoué",
		"open_session_success"				: u'Ouverture de session OK ',
		"open_session_fail"					: u"Echec de l'ouverture de session : Login ou mot de passe incorrect",
		"proadmin_connection_fail"			: u"La connexion à ProAdmin a échoué: Cette application n'existe pas sur le serveur ou l'identification est incorrecte ",
		"at"								: u'à',
		"test_sso_btn"						: u'Tester le SSO',
		"cancel_btn"						: u'Annuler',
		"close_btn"							: u'Fermer',
		"warning_test_sso"					: u"Vous allez être redirigé vers ProAdmin. Si un problèmre survient pressez le bouton retour de votre navigateur.",
		"success_sso"						: u'SSO est OK.',



		#errors
			"warning_title"					: u'Attention!',
			"error_title"					: u'Erreur!',
			"select_objects_error"			: u'Sélectionnez les objets',
			"fill_group_name_field"			: u'Spécifiez le nom du groupe',
			"group_name_already_exists"		: u'Un groupe portant ce nom existe déjà',
			"group_doesnt_exist"			: u"Le groupe n'existe pas",
			"fill_all_fields_with_star_error" : u"S'il vous plaît remplir tous les champs",
			"user_doesnt_exist_error"		: u"L'utilisateur n'existe pas. Actualisez la page.",
			"group_doesnt_exist_error"		: u"Le groupe n'existe pas. Actualisez la page.",
			"user_login_already_exist_error": u'Un utilisateur avec cet identifiant existe déjà',
			"user_email_is_incorrect_error" : u'Erreur adresse e-mail',
			"user_phone_illegal_characters"	: u'Numéro de téléphone incorrect',
			"user_password_is_empty_error"	: u'Entrez le mot de passe',
	"license" : 	u"""Veuillez lire et accepter ce contrat de licence avant d’installer et d’utiliser le software. Si vous êtes une personne physique, vous devez être majeure ou avoir une autorisation parentale. Si vous l’achetez pour le compte d'une entreprise, vous devez disposer des pouvoirs notariaux complets afin de légaliser ce contrat au nom de l'entreprise. En cliquant sur le bouton « Accepter » (ou équivalent) placé plus bas, vous accepterez ce contrat.
En exécutant {0}, vous acceptez implicitement les termes et les conditions du présent document, et également que vous connaissez {0} et que vous l’exécutez sous votre propre responsabilité.
VDOM Box International se réserve le droit de mettre à jour et de modifier la Licence de logiciel et tous documents de référence joints, le cas échéant.
Droits d’auteur\n
Ce logiciel et sa documentation sont la propriété de VDOM Box International. Il est interdit de les traduire, décompiler, modifier, adapter et corriger, ce qui inclut l’utilisation de toute technologie actuelle ou future. Il vous est interdit de supprimer ou modifier les informations de licence et de le transmettre à des tiers. La location et le prêt du logiciel sont interdits. Vous ne pouvez pas utiliser ce logiciel sur un autre matériel que celui fourni avec celui-ci. Seul l’auteur est habilité à effectuer ces opérations.\n
Le non-respect de l’un des termes et conditions de cette Licence sera interprété comme un non-respect de ce Contrat.\n
Garanties et responsabilités

Vous devez utiliser {0} conformément aux termes et aux conditions du présent document. VDOM Box International déclinera toute responsabilité concernant les dommages émanant de votre utilisation de {0} de manière contraire à cette Licence de logiciel.
À l’exception des responsabilités réglementaires établies par les lois de protection du consommateur, vous exemptez VDOM Box International de toute responsabilité émanant de l’exécution inadéquate de {0} ou du fonctionnement incorrect de {0} lié à votre manière d’exécuter le logiciel. Cette exemption de responsabilité s’étendra également aux employés et à la direction de VDOM Box International.
VDOM Box International stipule que cette Licence qui permet d’utiliser {0} n’enfreint aucun contrat préalable ou législation actuelle.
VDOM Box International garantit que {0} n’est pas un programme espion ou de publicité. VDOM Box International garantit également que {0} ne montre pas de publicités émergentes et ne compile pas non plus les données personnelles des utilisateurs.
VDOM Box International ne garantit pas la disponibilité, la continuité ni le fonctionnement à l’abri des fausses manœuvres de {0}. Par conséquent, dans la mesure où la législation le permet, cette garantie n’inclut pas les dommages émanant du manque de responsabilité ou fonctionnement ininterrompu de {0} et de tout service facilité à travers celui-ci.
VDOM Box International n’assume pas la responsabilité en cas de circonstance imprévisible ou de force majeure. De même, VDOM Box International ne sera pas responsable des causes hors du contrôle raisonnable telles que les virus et les interférences de tiers.
Vous exempterez VDOM Box International de toute responsabilité pour les droits de propriété intellectuelle, les droits de distribution, l’intégrité, la qualité et l’exécution du logiciel informatique téléchargé avec {0}.
Vous affirmez avoir pris connaissance du fait que VDOM Box International peut n’avoir aucun rapport avec les propriétaires des programmes informatiques que vous téléchargez. Vous exempterez VDOM Box International de toute responsabilité concernant toutes actions en justice intentées contre vous, liées à votre utilisation ou possession de produits téléchargés avec {0}, comprenant, mais sans se limiter à cela, les réclamations pour calomnies, violations de droits de protection des données ou publicité, droits de propriété intellectuelle, droits de nom commercial et toute autre action ou plainte se référant au contenu, à la qualité et au fonctionnement de ce logiciel.
Si vous effectuez une des opérations ci-dessus, vos droits d’utilisation sont automatiquement résiliés et l’auteur pourra ester en justice pour obtenir des dommages et intérêts.\n
Vous n’êtes pas autorisé à posséder des copies du fichier XML (généré par le serveur VDOM après l'installation du logiciel) représentant l’application sur d’autres supports de stockage que ceux inclus dans le matériel exécutant l’application. Vous n’êtes pas autorisé à faire de copies de la documentation papier.\n
Transfert de licence. Pour transférer la licence de ce logiciel sur un autre utilisateur unique, celle-ci doit d’abord être supprimée de la carte à puce du précédent utilisateur, ce transfert ne peut se faire que par le distributeur de cette licence.\n
En utilisant ce logiciel, vous vous engagez à respecter les droits d’auteur, et à veiller à ce que les autres utilisateurs les respectent aussi.\n
Ce logiciel est protégé en France par les lois sur la propriété intellectuelle ainsi qu’à l’étranger par les conventions internationales sur le droit d’auteur (convention de Berne).\n
La violation de l'un des droits de l'auteur du logiciel est un délit de contrefaçon sanctionnée en France par l'article L335-2 du code de la propriété intellectuelle.\n
Le logiciel est fourni tel quel, sans aucune garantie. L'auteur ne saurait voir sa responsabilité engagée en cas de dommages de quelque nature que ce soit subis par l'utilisateur ou des tiers et résultant directement ou indirectement de son utilisation, notamment la perte de données, ou toute perte financière résultant de son utilisation ou de l’impossibilité de l’utiliser, et ceci même si l’auteur a été prévenu de la possibilité de tels dommages. En tout état de cause, la responsabilité de l’auteur ne pourra excéder le montant payé pour l’acquisition ou l’utilisation de la licence.\n
Si le logiciel proposé est présenté comme étant une mise à jour, vous devez être déjà titulaire d’une licence antérieure du même logiciel pour pouvoir en bénéficier. Une mise à jour complète ou remplace la licence et la version antérieure du logiciel. La mise à jour et la licence originale doivent être considérées comme un produit unique. Vous n’êtes donc pas autorisé à les céder ou donner séparément.""",

	"license_button" : u"License",

	#license page
	"agree_button"				: u'Accepter',
	"disagree_button"			: u'Rfuser',
	"close_button"				: u'Fermer',
	"disagree_warning"			: u'Vous devez accepter cette licence pour utiliser le produit.',
	"select_operation_mode"		: u'Choisissez le mode de gestions des drotis :',
	"standalone_mode"			: u'Autonomme',
	"proadmin_mode"				: u'Via ProAdmin',
	"proadmin_page_warning"		: u'ProAdmin peut aussi être configuré dans le logiciel.',
	"go_button"					: u'Suivant',
	"password_title"			: u'Veuillez saisir le mot de passe administrateur :',
	"password_field"			: u'Mot de passe :',
	"confirm_password_field"	: u'Confirmer le mot de passe :',
	"apply_password"			: u'Appliquer',

	#proadmin_v2
	"system_login_title"			: u'Système login',
	"system_account"				: u'Compte système :',
	"login_btn"						: u'Login',
	"users_container_label"			: u'Utilisateur',
	"incorrect_login"				:u'Login ou mot de passe incorrecte',
	"no_vdom"						:u"Le serveur auquel vous vous connecté n'est pas de type VDOM",
	"standalone"					:u'Autonome',
	"proadmin_connection"			:u'Connecté à ProAdmin',
	"restart_connectoin_btn"		:u'Restart connection',
	"reset_btn"						:u'RAZ',
	"greating_title"				:u'Connecté en tant que %s',
	"account_column"				:u'Login',
	"name_column"					:u'Nom',
	"login_column"					:u'Se connecter en tant que',
	"standalone_text"				:u"Votre logiciel n'utilisera pas ProAdmin pour la gestion des droits, il fonctionnera en mode autonome",
	"proadmin_text"					:u"Votre logiciel utilisera ProAdmin pour la gestion des droits, celle-ci sera ainsi centralisée.",
	"logout_hint"					:u'Veuillez cliquer pour vous déconnecter',
	"user_not_logged_in"			:u"Vous n'êtes pas connecté...",
	"proadmin_management"			:u'Gestion ProAdmin',
	"user_management"				:u'Gestion des utilisateurs',


	#log off/start button
	"switch_to"						: u"Aller vers",
	"logout"						: u"Deconnexion",
	"logoff_caption"				: u"Deconnexion.",
	"logoff_message"				: u"Vous allez être redirigé vers la page de login dans quelques secondes.",

	#free_space
	"Gb"			:u'Go',
	"Mb"			:u'Mo',
	"of"			:u' de ',
	"free"			:u' Libre',
}

lang_rectangle = {
	#'id' 							: 	[ 	left,		top,	width,	height 	]
	"user_and_group_manage"	: {
		#top bar
			"top_bar_create_user_btn"		: 	[	"18", 	"85", 	"90", 	"35" 	],
			"top_bar_delete_selected_btn" 	: 	[ 	"118", 	"85", 	"98", 	"35" 	],
			"top_bar_add_to_group_btn"		: 	[ 	"226", 	"85", 	"84", 	"35" 	],
			"top_Bar_create_group_btn"		:	[	"18",	"85",	"88",	"35"	],

		#add to group dialog
			"add_to_group_to_title_text"	:	[ 	"17",	"155",	"15",	"14"	],

		#create user dialog
			"continue_btn"					:	[	"111",	"582",	"188",	"25"	],
			"add_groups_btn"				:	[	"14",	"27",	"140",	"32"	],
			"del_sel_groups_btn"			:	[	"160",	"27",	"170",	"32"	],

		#add user group dialog
			"add_ug_cancel_btn"				:	[	"218",	"397",	"80",	"33"	],
			"add_ug_add_btn"				:	[	"310",	"397",	"80",	"33"	],
			"selected_users_text"			:	[	"19",	"364",	"190",	"14"	],
			"selected_groups_text"			:	[	"8",	"446",	"140",	"14"	],
			"selected_users_count"			:	[	"215",	"364",	"50",	"14"	],
			"selected_groups_count"			:	[	"155",	"446",	"50",	"14"	],

			"objects_per_page_dropdown"		: 	[	"70",	"1",	"52",	"22"	],
		}
}
