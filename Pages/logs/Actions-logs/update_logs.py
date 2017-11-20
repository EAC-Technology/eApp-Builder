"""
"""

from ProSuiteLogsPage import ProSuiteLogsPage


page = ProSuiteLogsPage(self)
page.vdom_objects = {
    "growl": self.growl,
    "logs.data": self.logs_cnt.hpt,
    "logs.timer": self.update_timer,

}
page.run('update')