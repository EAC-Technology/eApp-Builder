from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

    from class_timer import Timer
    from class_custom_event import CustomEvent
    from class_macro import Macros
    import json, localization
    from class_plugins import Plugins
    from config import config
    from VEE_events import event_map


    lang = localization.get_lang()

    macros_id = request.shared_variables["macro_id"]
    plugin_id = request.shared_variables["plugin_id"]
    plugin = Plugins.get_by_id(plugin_id)


    macro_type = request.arguments.get( "itemValue", Macros.MacrosType.UNKNOWN )


    def setup_event_type_controls():
        self.dialog_create_macro.form_macro.container_back.formlist_location.visible = "0"
        self.dialog_create_macro.form_macro.container_back.text_location.visible = "0"
        self.dialog_create_macro.form_macro.container_back.formlist_event.visible = "1"
        self.dialog_create_macro.form_macro.container_back.text_event.visible = "1"
        self.dialog_create_macro.form_macro.container_back.formlist_page.visible = "0"
        self.dialog_create_macro.form_macro.container_back.text_timer.visible = "0"

        event_dict = {}
        for event in event_map:
            event_dict[event] = lang[event_map[event].__name__]

        for timer in Timer.get_timer_by_plugin_guid(plugin.guid):
            event_dict[timer.guid] = timer.name

        for cevent in CustomEvent.get_custom_event_by_plugin_guid(plugin.guid):
            event_dict[cevent.guid] = cevent.name

        self.dialog_create_macro.form_macro.container_back.formlist_event.value = json.dumps(event_dict)


    def setup_button_type_controls():
        self.dialog_create_macro.form_macro.container_back.formlist_page.selectedvalue = config["plugin_page_dict"].keys()[0]
        self.dialog_create_macro.form_macro.container_back.formlist_page.value = json.dumps(config["plugin_page_dict"])
        self.dialog_create_macro.form_macro.container_back.formlist_location.visible = "1"
        self.dialog_create_macro.form_macro.container_back.text_location.visible = "1"
        self.dialog_create_macro.form_macro.container_back.formlist_event.visible = "0"
        self.dialog_create_macro.form_macro.container_back.text_event.visible = "0"
        self.dialog_create_macro.form_macro.container_back.formlist_location.value = json.dumps({"1" : "On panel", "2" : "In plugin menu"})


    def setup_library_type_controls():
        self.dialog_create_macro.form_macro.container_back.formlist_page.visible = "0"
        self.dialog_create_macro.form_macro.container_back.formlist_location.visible = "0"
        self.dialog_create_macro.form_macro.container_back.text_location.visible = "0"
        self.dialog_create_macro.form_macro.container_back.formlist_event.visible = "0"
        self.dialog_create_macro.form_macro.container_back.text_event.visible = "0"
        self.dialog_create_macro.form_macro.container_back.text_timer.visible = "0"


    if macros_id and macro_type == Macros.MacrosType.UNKNOWN:

        macros = Macros.get_by_id(macros_id)

        self.dialog_create_macro.form_macro.formtext_id.value = macros_id
        self.dialog_create_macro.form_macro.formtext_name.value = macros.name
        self.dialog_create_macro.form_macro.formtextarea_description.value = macros.description
        macro_type = macros.type

        if macros.type == Macros.MacrosType.EVENT:
            setup_event_type_controls()

            if macros.timer_guid:
                self.dialog_create_macro.form_macro.container_back.formlist_event.selectedvalue = macros.timer_guid
            elif macros.custom_event_guid:
                self.dialog_create_macro.form_macro.container_back.formlist_event.selectedvalue = macros.custom_event_guid
            elif macros.class_name:
                for event in event_map:
                    if event_map[event].__name__ == macros.class_name:
                        self.dialog_create_macro.form_macro.container_back.formlist_event.selectedvalue = event
                        break

        elif macros.type == Macros.MacrosType.BUTTON:
            setup_button_type_controls()
            self.dialog_create_macro.form_macro.container_back.formlist_location.selectedvalue = "1" if macros.on_board == "1" else "2"
            self.dialog_create_macro.form_macro.container_back.formlist_page.selectedvalue = macros.page

        else:
            setup_library_type_controls()



    self.dialog_create_macro.form_macro.container_back.formlist_type.value = json.dumps({
        Macros.MacrosType.EVENT: "Event macro",
        Macros.MacrosType.BUTTON: "Button macro",
        Macros.MacrosType.LIBRARY: "Library"
    })

    if macro_type == Macros.MacrosType.UNKNOWN:
        macro_type = Macros.MacrosType.EVENT

    self.dialog_create_macro.form_macro.container_back.formlist_type.selectedvalue = macro_type

    if macro_type == Macros.MacrosType.BUTTON:
        setup_button_type_controls()

    elif macro_type in Macros.MacrosType.EVENT:
        setup_event_type_controls()

    else:
        setup_library_type_controls()



main()
