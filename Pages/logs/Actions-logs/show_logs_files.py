"""
"""

from ProSuiteLogsPage import ProSuiteLogsPage


page = ProSuiteLogsPage(self)
page.vdom_objects = {
    "growl": self.growl,
    "dialogs.download": self.dwnload_logs_dialog,
    "dialogs.download.files": self.dwnload_logs_dialog.files_cnt.files_hpt,
}
page.run('files')