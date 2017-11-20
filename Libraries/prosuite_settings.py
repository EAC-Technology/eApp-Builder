"""
"""

import logging


DEBUG = True


default_settings = {
    "pages": {
        "cleaner": "/cleaner",
        "home": "/home",
        "local_ug": "/users_and_groups",
        "login": "/login",
        "logoff": "/logoff",
        "logs": "/logs",
        "plugins": "/plugins",
        "plugin_details": "/plugin_details",
        "plugin_source": "/macros_source",
        "rules": "/rules",
        "remote_scheme": "/remote_scheme",
        "remote_ug": "/remote_users_and_groups",
        "server500": "/server500",
        "settings": "/settings",
    },
    "system": {
        "debug": DEBUG,
        "login_as": DEBUG and 'root',
        "root_god_mode": DEBUG,
    },
    "logging": {
        "level": logging.DEBUG if DEBUG else logging.INFO,
        "file": "logs/app_log", # path to logs
        "max_size": 1048576, # in bytes
        "parts": 10, # max files
        "max_mem_records": 512,
    },
    "app_info": {
        "name": u"ProMail",
        "version": u"1.10.0",
        "commit": u"e123e2134",
        "template_version": u"1.0.0",
        "template_commit": u"e423r445",
        "id": application.id
    },
    "localization": {
        "page_title": u"{page_name} - {app_name}",
    },
    "background_tasks_manager": {
        "max_run_time": 3600,
        "max_attempts": 5,
    },
    "databases": {
        "path": "databases",
    }
}


class Settings(object):

    pages = default_settings["pages"]
    system = default_settings["system"]
    info = default_settings["app_info"]
    localization = default_settings["localization"]
    logging = default_settings["logging"]
    tasks_manager = default_settings["background_tasks_manager"]
    databases = default_settings["databases"]


settings = Settings
