import logging

from pytest_tui.utils import (
    TUI_FOLD_CONTENT_BEGIN,
    TUI_FOLD_CONTENT_END,
    TUI_FOLD_TITLE_BEGIN,
    TUI_FOLD_TITLE_END,
)

# import logging
# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

# from haggis import logs as haggis_logs
# haggis_logs.add_logging_level("FOLD", logging.WARNING + 1)
# logging.getLogger(__name__)


# class CustomHandler(logging.Handler):
#     def __init__(self):
#         super().__init__()

#     def emit(self, record):
#         log_entry = self.format(record)
#         # Here you could define how you want to handle the log entry,
#         # for example, writing to a file, sending an email, or printing to the console.
#         print(f"GO AHEAD {log_entry}")


class TitleLogger(logging.getLoggerClass()):
    """Custom logger class to add TUI fold title formatting to log messages."""

    def __init__(self, name, level=logging.ERROR):
        super().__init__(name, level)
        # self.addHandler(CustomHandler)

    def _log(self, level, msg, args, exc_info=None):
        msg = TUI_FOLD_TITLE_BEGIN + msg + TUI_FOLD_TITLE_END
        super()._log(level, msg, args, exc_info)


class ContentBeginLogger(logging.getLoggerClass()):
    """Custom logger class to add TUI fold content-begin formatting to log messages."""

    def __init__(self, name, level=logging.ERROR):
        super().__init__(name, level)
        # self.addHandler(CustomHandler)

    def _log(self, level, msg, args, exc_info=None):
        msg = TUI_FOLD_CONTENT_BEGIN + msg
        super()._log(level, msg, args, exc_info)


class ContentLogger(logging.getLoggerClass()):
    """Custom logger class to add TUI fold interim content formatting to log messages.
    """

    def __init__(self, name, level=logging.ERROR):
        super().__init__(name, level)
        # self.addHandler(CustomHandler)

    def _log(self, level, msg, args, exc_info=None):
        super()._log(level, msg, args, exc_info)


class ContentEndLogger(logging.getLoggerClass()):
    """Custom logger class to add TUI fold content-end formatting to log messages."""

    def __init__(self, name, level=logging.ERROR):
        super().__init__(name, level)
        # self.addHandler(CustomHandler)

    def _log(self, level, msg, args, exc_info=None):
        msg = msg + TUI_FOLD_CONTENT_END
        super()._log(level, msg, args, exc_info)


class TuiLoggers:
    """
    Custom logger class to add TUI fold formatting to log messages.
    This formatting is consumed by html_gen.py in order to generate
    a folded line for each log message usng the TUI fold feature.

    Attributes:
        title_logger (TitleLogger): logger for TUI fold title
        content_begin_logger (ContentBeginLogger): logger for TUI fold content-begin
        content_logger (ContentLogger): logger for TUI fold interim content
        content_end_logger (ContentEndLogger): logger for TUI fold content-end

    Methods:
        localize(name=__name__, level=logging.WARNING): localize the loggers to the current module
        get_tui_loggers(): return the loggers

    Usage:
    >>> from pytest_tui.tui_logger import TuiLoggers
    >>> tui_loggers = TuiLoggers()
    >>> tui_loggers.localize(name=__name__, <level=LEVEL>)
    >>> title_logger, content_begin_logger, content_logger, content_end_logger = tui_loggers.get_tui_loggers()

    >>> logger.info(msg)  # non-folding, regular log message, if defined in test
    >>> title_logger.warning("Title")  #
    >>> content_begin_logger.warning("Content Begin")  # non-folding, regular log message
    >>> content_logger.warning("Content")  # non-folding, regular log message
    >>> content_end_logger.warning("Content End")  # non-folding, regular log message
    """

    def __init__(self):
        self.title_logger = TitleLogger
        self.content_begin_logger = ContentBeginLogger
        self.content_logger = ContentLogger
        self.content_end_logger = ContentEndLogger

    def localize(self, name=__name__, level=logging.WARNING):
        for tui_logger in self.get_tui_loggers():
            tui_logger.name = name
            tui_logger.setLevel(level)

    def get_tui_loggers(self):
        tui_loggers = []
        for tui_logger in (
            TitleLogger,
            ContentBeginLogger,
            ContentLogger,
            ContentEndLogger,
        ):
            logging.setLoggerClass(tui_logger)
            tui_loggers.append(logging.getLogger(logging.getLoggerClass().__name__))
        return tui_loggers
