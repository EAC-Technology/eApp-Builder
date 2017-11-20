"""
"""

from ProSuiteLogsPage import ProSuiteLogsPage


page = ProSuiteLogsPage(self)
page.vdom_objects = {
    "growl": self.growl,
    "logs.data": self.logs_cnt.hpt,

    "topbar.download.btn": self.dwnloadlogs_btn,
    "topbar.autoupdate.btn": self.autoupdate.checkbtn,

    "dialogs.download": self.dwnload_logs_dialog,
    "dialogs.download.close": self.dwnload_logs_dialog.close_btn,

    "popup.loglevel": self.loglevelsform,
    "popup.loglevel.form": self.loglevelsform,
    "popup.loglevel.form.list": self.loglevelsform.lv,
    "popup.loglevel.form.hide": self.loglevelsform.hidebtn,
    "popup.loglevel.form.reset": self.loglevelsform.resetbtn,
    "popup.loglevel.form.submit": self.loglevelsform.submitbtn,

    "popup.loggers": self.loggersform,
    "popup.loggers.form": self.loggersform,
    "popup.loggers.form.list": self.loggersform.lg,
    "popup.loggers.form.reset": self.loggersform.resetbtn,
    "popup.loggers.form.hide": self.loggersform.hidebtn,
    "popup.loggers.form.submit": self.loggersform.submitbtn,
}

page.run('onload')