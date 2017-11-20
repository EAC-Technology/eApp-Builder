from widget_user_group_dialog import authenticated, error_handler, administrator
import widget_user_group_dialog
widget_user_group_dialog.vdom_container = self


@authenticated
@administrator
@error_handler
def main():

    from class_macro import Macros
    from class_timer import Timer
    from class_custom_event import CustomEvent
    from widget_plugins import WidgetPlugins
    from widget_macro import WidgetMacros
    from class_plugins import Plugins
    import localization

    lang = localization.get_lang()

    from VEE_events import event_map


    name = self.dialog_create_macro.form_macro.formtext_name.value = request.arguments.get("formtext_name", "")
    macros_type = self.dialog_create_macro.form_macro.container_back.formlist_type.selectedvalue = request.arguments.get("formlist_type", Macros.MacrosType.LIBRARY)
    event = self.dialog_create_macro.form_macro.container_back.formlist_event.selectedvalue = request.arguments.get("formlist_event", "")
    location = self.dialog_create_macro.form_macro.container_back.formlist_location.selectedvalue = request.arguments.get("formlist_location", "")
    description = self.dialog_create_macro.form_macro.formtextarea_description.value = request.arguments.get("formtextarea_description", "")
    macros_id = self.dialog_create_macro.form_macro.formtext_id.value = request.arguments.get("formtext_id", "")
    page = self.dialog_create_macro.form_macro.container_back.formlist_page.selectedvalue = request.arguments.get("formlist_page", "")

    import re
    guid_regex = re.compile("^[a-zA-Z0-9]{8}\-[a-zA-Z0-9]{4}\-[a-zA-Z0-9]{4}\-[a-zA-Z0-9]{4}\-[a-zA-Z0-9]{12}$")

    class_name = ""
    timer_guid = ""
    custom_event_guid = ""
    is_button = "0"
    on_board = "0"

    if macros_type == Macros.MacrosType.EVENT:
        is_button = "0"
        if guid_regex.match(event):
            if Timer.get_timer_by_guid(event):
                timer_guid = event
                class_name = "VEE_TimerEvent"
            elif CustomEvent.get_custom_event_by_guid(event):
                custom_event_guid = event
                class_name = "VEE_CustomEvent"
        else:
            for e in event_map:
                if e == int(event):
                    class_name = event_map[e].__name__

    elif macros_type == Macros.MacrosType.BUTTON:
        is_button = "1"
        on_board = "1" if location and location == "1" else "0"

    elif macros_type != Macros.MacrosType.LIBRARY:
        macros_type = Macros.MacrosType.LIBRARY


    plugin_id = request.shared_variables["plugin_id"]
    plugin = Plugins.get_by_id(plugin_id)
    macros = Macros.get_by_id(macros_id) if macros_id else Macros()
    macros.name         = name
    macros.class_name   = class_name
    macros.timer_guid = timer_guid
    macros.custom_event_guid = custom_event_guid
    macros.is_button_macros = is_button
    macros.on_board = on_board
    macros.description = description
    macros.plugin_guid = plugin.guid
    macros.page = page
    macros.type = macros_type
    macros.save()

    plugin = Plugins.get_by_id(plugin_id)
    macros = plugin.get_macros()

    widget_macros = WidgetMacros()
    widget_macros.set_data(macros)
    widget_macros.render(self.datatable_macros)
    self.dialog_create_macro.action("hide", [])


main()
