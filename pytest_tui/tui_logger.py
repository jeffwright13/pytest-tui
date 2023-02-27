import logging
from pytest_tui.utils import TUI_FOLD_TITLE_BEGIN, TUI_FOLD_TITLE_END, TUI_FOLD_CONTENT_BEGIN, TUI_FOLD_CONTENT_END

class TitleLogger(logging.getLoggerClass()):
    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)

    def _log(self, level, msg, args, exc_info=None):
        msg = TUI_FOLD_TITLE_BEGIN + msg + TUI_FOLD_TITLE_END
        super()._log(level, msg, args, exc_info)

class ContentBeginLogger(logging.getLoggerClass()):
    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)

    def _log(self, level, msg, args, exc_info=None):
        msg = TUI_FOLD_CONTENT_BEGIN + msg
        super()._log(level, msg, args, exc_info)

class ContentLogger(logging.getLoggerClass()):
    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)

    def _log(self, level, msg, args, exc_info=None):
        msg = TUI_FOLD_CONTENT_BEGIN + msg + TUI_FOLD_CONTENT_END
        super()._log(level, msg, args, exc_info)

class ContentEndLogger(logging.getLoggerClass()):
    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)

    def _log(self, level, msg, args, exc_info=None):
        msg = msg + TUI_FOLD_CONTENT_END
        super()._log(level, msg, args, exc_info)
