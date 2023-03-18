import logging

from haggis import logs as haggis_logs

from pytest_tui.utils import (
    TUI_FOLD_CONTENT_BEGIN,
    TUI_FOLD_CONTENT_END,
    TUI_FOLD_TITLE_BEGIN,
    TUI_FOLD_TITLE_END,
)

haggis_logs.add_logging_level("FOLD", logging.INFO - 1)
logging.getLogger(__name__).setLevel("FOLD")


# class CustomHandler(logging.Handler):
#     def __init__(self):
#         super().__init__()

#     def emit(self, record):
#         msg = self.format(record)
#         print(msg)


class TitleLogger(logging.getLoggerClass()):
    """Custom logger class to add TUI fold title formatting to log messages."""

    def __init__(self, name, level=logging.FOLD):
        super().__init__(name, level)
        # self.addHandler(CustomHandler)

    def _log(self, level, msg, args, exc_info=None):
        msg = TUI_FOLD_TITLE_BEGIN + msg + TUI_FOLD_TITLE_END
        super()._log(level, msg, args, exc_info)


class ContentBeginLogger(logging.getLoggerClass()):
    """Custom logger class to add TUI fold content-begin formatting to log messages."""

    def __init__(self, name, level=logging.FOLD):
        super().__init__(name, level)
        # self.addHandler(CustomHandler)

    def _log(self, level, msg, args, exc_info=None):
        msg = TUI_FOLD_CONTENT_BEGIN + msg
        super()._log(level, msg, args, exc_info)


class ContentLogger(logging.getLoggerClass()):
    """Custom logger class to add TUI fold interim content formatting to log messages.
    """

    def __init__(self, name, level=logging.FOLD):
        super().__init__(name, level)
        # self.addHandler(CustomHandler)

    def _log(self, level, msg, args, exc_info=None):
        super()._log(level, msg, args, exc_info)


class ContentEndLogger(logging.getLoggerClass()):
    """Custom logger class to add TUI fold content-end formatting to log messages."""

    def __init__(self, name, level=logging.FOLD):
        super().__init__(name, level)
        # self.addHandler(CustomHandler)

    def _log(self, level, msg, args, exc_info=None):
        msg = msg + TUI_FOLD_CONTENT_END
        super()._log(level, msg, args, exc_info)
