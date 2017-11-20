import ProAdmin
import localization

lang = localization.get_lang()

ProAdmin.unregister_default_scheme()
ProAdmin.scheme()
self.container_remote_state.container_proadmin.text_last_sync.value = lang["last_sync_text"] + ( str(ProAdmin.scheme().sync_datetime.strftime("%H:%M:%S %d.%m.%Y")) if ProAdmin.scheme().sync_datetime else "?" )
self.container_remote_state.container_proadmin.text_sync_status.value = lang["syns_state_text"] + "OK" if ProAdmin.scheme().is_sync_active() else lang["syns_state_text"] + "FAIL"
self.container_remote_state.container_proadmin.text_objects.value = lang["object_text"] + str(len( ProAdmin.application().child_objects( recursive=True ) ))
self.container_remote_state.container_proadmin.text_users.value = lang["user_text"] + str(len( ProAdmin.application().get_users() ))