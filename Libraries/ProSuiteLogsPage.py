"""
"""

__version__ = "1.0.1"
__lastmod__ = "10/30/2015 23:45 (RTZ +5)"

import copy
import json
import logging
import os
import time

from collections import OrderedDict

from ext_enum import Enum
from prosuite_logging import logs_in_memory, manager as logs_manager, app_logger
from prosuite_utils import CachedProperty, escape_w_quote
from prosuite_web import ProSuiteBasicPage, administrator_only,\
                         authenticated, callback

# Shared Variables
LAST_RECORD_SV = "logs.lastrecord"
LOG_LEVEL_SV = "logs.level"
LOGGERS_SV = "logs.loggers"


LOGS_TIMER_UPDATE = 5000


TIME_CONVERTER = time.localtime


LOG_ROW_TEMPLATE = (u"<tr><td class='text-center cut-out-text'>{datetime}</td>"
                    u"<td class='text-center cut-out-text'>{lvl}</td>"
                    u"<td class='cut-out-text'>{name}</td><td><div><pre>{msg}</pre></div>"
                    u"</td></tr>")


class LogLevel(Enum):

    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG



class ProSuiteLogsPage(ProSuiteBasicPage):

    @callback('request_start', 2)
    @authenticated
#    @administrator_only
    def on_request_start(self, *args, **kwargs):
        pass

    @callback('onload', 2)
    def onload(self, *args, **kwargs):
        """
        On page loading
        """
        try:
            download_f = int(self.get_argument("download", None))

        except Exception as  ex:
            download_f = None

        if download_f is not None:
            self.get_log_file(download_f)
            return

        self.render_logs_table()
        self.render_loggers()
        self.render_log_levels()


    @callback('update', 1)
    def update_logs(self, *args, **kwargs):
        """
        Refresh logs data
        """
        self.page.action("custom", [u"{}({})".format(
            self.logs_update_js_func,
            json.dumps(escape_w_quote(self.logs_to_html())))
        ])

        self.vdom_objects["logs.timer"].action("start", [LOGS_TIMER_UPDATE])

    @callback('files', 1)
    def show_log_files(self, *args, **kwargs):
        """
        Show list of available log files
        """
        path_to_logs = application.storage.abs_path(os.path.dirname(self.app_settings.logging["file"]))
        files = sorted(os.listdir(path_to_logs))
        files_html = [u"""<li><a href="?download={}">{}</a></li>""".format(i, files[i]) for i in range(0, len(files))]

        self.vdom_objects["dialogs.download.files"].htmlcode = "".join(files_html)
        self.vdom_objects["dialogs.download"].action("show", [""])


    @CachedProperty
    def datetime_format(self):
        return self.localization["global.datetime_format"]

    @CachedProperty
    def record_formatter(self):
        return logs_in_memory.format

    @CachedProperty
    def logs_update_js_func(self):
        return "setLogsToTable" if self.get_argument("formid", "") else \
               "appendLogsToTable"

    @CachedProperty
    def _available_loggers(self):
        return [logger for logger in logs_manager.loggerDict.keys() \
                 if logger.startswith(app_logger.name)]

    @property
    def available_loggers(self):
        return self._available_loggers


    @CachedProperty
    def _last_record_ts(self):
        # timestamp of last displayed record
        last_record_ts = 0.0

        # if there is no submitted form get value from SV
        # or from request args
        if not self.get_argument("formid", ""):
            try:
                last_record_ts = float(self.get_argument("ts", 0.0) or self.shared_vars.get(LAST_RECORD_SV, 0.0))
            except:
                pass

        self.shared_vars[LAST_RECORD_SV] = last_record_ts

        return last_record_ts

    @property
    def last_record_ts(self):
        return self._last_record_ts

    @last_record_ts.setter
    def last_record_ts(self, value):
        self._last_record_ts = self.shared_vars[LAST_RECORD_SV] = value


    @CachedProperty
    def _log_level(self):
        # check is arg in request or not
        log_level = self.get_argument("lv", "")

        # if it is action check is form submitted or not
        if self.is_action():

            if self.get_argument("formid", "") == "loglevel":

                try:
                    log_level = json.loads(log_level)
                except:
                    log_level = log_level

            else:
                # exception will be raised only
                # if such arg is not in request args
                log_level = self.shared_vars.get(LOG_LEVEL_SV, None)

        else:
            log_level = log_level.split(",")

        if not isinstance(log_level, (list, tuple)):
            log_level = [log_level]

        result = []
        for level in log_level:
            if level:
                try:
                    result.append(LogLevel(int(level)).value)
                except:
                    pass

        if result:
            self.shared_vars[LOG_LEVEL_SV] = result

        else:
            self.shared_vars[LOG_LEVEL_SV] = None

        return result

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        self._log_level = self.shared_vars[LOG_LEVEL_SV] = value


    @CachedProperty
    def _loggers(self):
        # check is arg in request or not
        loggers = self.get_argument("lg", "")

        # if it is action check is form submitted or not
        if self.is_action():

            if self.get_argument("formid", "") == "logger":

                try:
                    loggers = json.loads(loggers)
                except:
                    loggers = loggers.encode('utf8')

            else:
                # exception will be raised only
                # if such arg is not in request args
                loggers = self.shared_vars.get(LOGGERS_SV, None)

        else:
            loggers = loggers.split(",")

        if not isinstance(loggers, (list, tuple)):
            loggers = [loggers]

        # add all child loggers
        logger_set = set()
        for l in loggers:
            if isinstance(l, unicode):
                l = l.encode("utf8")
            logger_set.add(l)
            for a in self.available_loggers:
                if a.startswith(l):
                    logger_set.add(a)
        loggers = list(logger_set)

        loggers = [logger for logger in loggers if logger in self.available_loggers]
        if loggers:
            self.shared_vars[LOGGERS_SV] = loggers

        else:
            self.shared_vars[LOGGERS_SV] = None

        return loggers

    @property
    def loggers(self):
        return self._loggers

    @loggers.setter
    def loggers(self, value):
        self._loggers = self.shared_vars[LOGGERS_SV] = value



    def format_time(self, record):
        """
        Format record's timestamp
        """
        return time.strftime(self.datetime_format, TIME_CONVERTER(record.created))

    def format_record(self, record):
        """
        Render logs record
        """
        try:
            msg = escape_w_quote(self.record_formatter(record))
        except:
            msg = self.localization["prosuite.logs.table.msg.error.cantformat"]

        return LOG_ROW_TEMPLATE.format(
            datetime=self.format_time(record),
            lvl=record.levelname,
            name=record.name.decode('utf8'),
            msg=msg
        )

    def logs_to_render(self):
        """
        Return filtered logs list
        """
        # copy logs to avoid mutations during iterations
        logs = copy.copy(logs_in_memory.buffer)

        if self.last_record_ts and logs:
            logs = filter(lambda rec: rec.relativeCreated > self.last_record_ts, logs)

        if self.log_level and logs:
            logs = filter(lambda rec: rec.levelno in self.log_level, logs)

        if self.loggers and logs:
            logs = filter(lambda rec: rec.name in self.loggers, logs)

        return logs

    def logs_to_html(self):
        """
        Render logs data to HTML
        """
        logs = self.logs_to_render()

        out =  "".join(map(self.format_record, reversed(logs)))

        if logs:
            self.last_record_ts = logs[-1].relativeCreated

        return out

    def render_logs_table(self):
        """
        Render logs table
        """
        self.vdom_objects["logs.data"].htmlcode = self.vdom_objects["logs.data"].htmlcode.format(
            th_date=self.localization["prosuite.logs.table.header.date"],
            th_lvl=self.localization["prosuite.logs.table.header.lvl"],
            th_name=self.localization["prosuite.logs.table.header.name"],
            th_msg=self.localization["prosuite.logs.table.header.msg"],
            table_body=self.logs_to_html()
        )

    def render_loggers(self):
        loggers = sorted(self.available_loggers)
        spacer = "-"

        result = OrderedDict()
        for logger in loggers:
            chain = logger.split(".")
            result[logger] = u"{} {}".format(
                spacer * (len(chain) - 1),
                chain[-1].decode('utf8')
            )

        self.vdom_objects["popup.loggers.form.list"].value = json.dumps(result)
        if self.loggers:
            self.vdom_objects["popup.loggers.form.list"].selectedvalue = json.dumps(self.loggers)

    def render_log_levels(self):
        self.vdom_objects["popup.loglevel.form.list"].value = json.dumps({
            str(lvl.value): logging.getLevelName(lvl.value) for lvl in LogLevel
        })
        if self.log_level:
            self.vdom_objects["popup.loglevel.form.list"].selectedvalue = json.dumps(map(str, self.log_level))

    def get_log_file(self, fnum):
        """
        Send in response requested log file
        """
        fname_suffix = ".{}.gz".format(fnum) if fnum else ""
        fname = self.app_settings.logging["file"] + fname_suffix

        if application.storage.exists(fname):
            response.send_file(os.path.split(fname)[1], application.storage.getsize(fname), application.storage.open(fname))

    def get_page_title(self):
        return self.localization["prosuite.logs.title"]

    def get_localization_data(self):
        return {
            self.vdom_objects["topbar.download.btn"]: "prosuite.logs.header.download_logs",
            self.vdom_objects["topbar.autoupdate.btn"]: "prosuite.logs.header.autoupdate.button",
            self.vdom_objects["dialogs.download"]: "prosuite.logs.download_logs.title",
            self.vdom_objects["dialogs.download.close"]: "prosuite.logs.download_logs.close",
            self.vdom_objects["popup.loglevel.form.hide"]: "prosuite.logs.popup.loglevel.hide",
            self.vdom_objects["popup.loglevel.form.reset"]: "prosuite.logs.popup.loglevel.reset",
            self.vdom_objects["popup.loglevel.form.submit"]: "prosuite.logs.popup.loglevel.submit",
            self.vdom_objects["popup.loggers.form.hide"]: "prosuite.logs.popup.loggers.hide",
            self.vdom_objects["popup.loggers.form.reset"]: "prosuite.logs.popup.loggers.reset",
            self.vdom_objects["popup.loggers.form.submit"]: "prosuite.logs.popup.loggers.submit",
        }
