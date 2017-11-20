"""
"""

import cStringIO
import gzip
import logging
import os
import sys
import traceback
import weakref

from collections import deque
from logging.handlers import RotatingFileHandler

from prosuite_settings import settings


class DequeMemoryHandler(logging.Handler):
    """
    A handler class which buffers logging records in memory. Whenever each
    record is added to the buffer, a check is made to see if the buffer should
    be flushed. If it should, then flush() is expected to do what's needed.
    """

    def __init__(self, capacity):
        """
        Initialize the handler with the buffer size.
        """
        logging.Handler.__init__(self)
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def emit(self, record):
        """
        Emit a record
        """
        self.buffer.append(record)

    def flush(self):
        """
        Override to implement custom flushing behaviour.

        This version just zaps the buffer to empty.
        """
        self.buffer.clear()

    def close(self):
        """
        Close the handler.

        This version just flushes and chains to the parent class' close().
        """
        try:
            self.flush()
        finally:
            logging.Handler.close(self)

    def handle(self, record):
        """
        Conditionally emit the specified logging record.

        Emission depends on filters which may have been added to the handler.
        Returns whether the filter passed the record foremission.
        """
        rv = self.filter(record)
        if rv:
            self.emit(record)
        return rv


class RotatingGzipFileHandler(RotatingFileHandler):

    def doRollover(self):
        """
        Do a rollover and gzip file
        """
        if self.stream:         # close existing stream
            self.stream.close()
            self.stream = None

        if self.backupCount > 0:       # iterate over existing file
            for i in range(self.backupCount - 1, 0, -1):
                sfn = "%s.%d.gz" % (self.baseFilename, i)
                dfn = "%s.%d.gz" % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    #print "%s -> %s" % (sfn, dfn)
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)

            dfn = self.baseFilename + ".1.gz"
            if os.path.exists(dfn):
                os.remove(dfn)

            # Issue 18940: A file may not have been created if delay is True.
            if os.path.exists(self.baseFilename):
                sfh = open(self.baseFilename, "rb")
                dfh = gzip.open(dfn, "wb")
                dfh.writelines(sfh)
                dfh.close()
                sfh.close()
                os.remove(self.baseFilename)

        if not self.delay:
            self.stream = self._open()


class ExcPlusFormatter(logging.Formatter):
    """
    """
    def format(self, record):
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self._fmt % record.__dict__
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not hasattr(record, "exc_text_ext"):
                setattr(record, "exc_text_ext", self.formatException(record.exc_info))

        if getattr(record, "exc_text_ext", None) :
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text_ext
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text_ext is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                s = s + record.exc_text_ext.decode(sys.getfilesystemencoding(),
                                               "replace")
        return s

    def formatException(self, ei):
        """
        Format and return the specified exception information as a string.

        This default implementation just uses
        traceback.print_exception()
        """
        tb = sys.exc_info()[2]
        while 1:
            if not tb.tb_next:
                break
            tb = tb.tb_next

        stack = []
        f = tb.tb_frame
        while f:
            stack.append(f)
            f = f.f_back

        stack = reversed(stack)

        sio = cStringIO.StringIO()
        traceback.print_exception(ei[0], ei[1], ei[2], None, sio)

        sio.write("%s\n%s" % ("*"*10, "Locals by frame, innermost last"))
        for frame in stack:
            sio.write("\n\nFrame \"%s\" in %s:%s at line %s:" % (
                frame.f_code.co_name,
                frame.f_code.co_filename,
                frame.f_code.co_firstlineno,
                frame.f_lineno
            ))

            for key, value in frame.f_locals.items():
                sio.write("\n\t%20s = " % key)
                #We have to be careful not to cause a new error in our error
                #printer! Calling str() on an unknown object could cause an
                #error we don't want.
            try:
                sio.write("%s :: %s" % (str(type(value)), str(value)))
            except:
                sio.write("<ERROR WHILE PRINTING VALUE>")

        sio.write("\n\n")
        traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
        sio.write("%s\n" % ("*"*10))

        s = sio.getvalue()
        sio.close()

        return s


class ProSuiteRootLogger(logging.Logger):
    """
    """
    def getChild(self, suffix):
        return self.manager.getLogger(suffix)


# Create unique root logger
manager = logging.Manager(None)
manager.setLoggerClass(ProSuiteRootLogger)

root_logger = manager.getLogger("System")
root_logger.setLevel(settings.logging["level"])
root_logger.manager = manager

manager.root = weakref.proxy(root_logger)
manager.setLoggerClass(logging.Logger)

# create rotating logs handler
logs_path = application.storage.abs_path(settings.logging["file"])
logs_dir = os.path.dirname(logs_path)

try:
    os.stat(logs_dir)
except Exception as ex:
    application.storage.mkdir(logs_dir)


rotating_hdlr = RotatingGzipFileHandler(
    logs_path,
    maxBytes=settings.logging["max_size"],
    backupCount=settings.logging["parts"]
)

# create default formatting
default_fmt = ExcPlusFormatter("%(asctime)s :: %(name)-12s :: %(levelname)-8s :: %(thread)s :: %(message)s")
rotating_hdlr.setFormatter(default_fmt)
root_logger.addHandler(rotating_hdlr)


# !!! this raise exception in application_onstart global action !!!
# root_logger.info("Logging system setup for application %s [%s] done!",
    # application.name,
    # application.id
# )

root_logger.info("Logging level is %s", logging.getLevelName(settings.logging["level"]))

# create application level logger
app_logger = root_logger.getChild(settings.info["name"])

# setup logs which will be stored in memory
logs_in_memory = DequeMemoryHandler(capacity=settings.logging["max_mem_records"])
app_logger.addHandler(logs_in_memory)

app_logger.info("Application logger created!")

