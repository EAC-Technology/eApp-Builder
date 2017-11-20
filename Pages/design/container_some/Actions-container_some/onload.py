import localization

lang = localization.get_lang()
session["tabViewUG"] = self.tabview1.id

#set interface language
self.form_search.some_text.value = lang["find_usr_title"]
self.tabview1.container_group.title = lang["add_usrgrp_diaolg_grp_tab_title"]
self.tabview1.container_user.title = lang["add_usrgrp_diaolg_usr_tab_title"	]
