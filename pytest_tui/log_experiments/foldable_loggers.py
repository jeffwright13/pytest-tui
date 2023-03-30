import logging
from typing import Any, Tuple, Union

from pytest_tui.utils import TUI_FOLD_TITLE_BEGIN, TUI_FOLD_TITLE_END


class FoldableLogger(logging.getLoggerClass()):
    """A logger that logs everything DEBUG level and above"""

    def __init__(self, name: str, level: int) -> None:
        self.level = level
        super().__init__(name, level)
        self.foldable_message = ""

    def send_foldable_message(self) -> None:
        super()._log(self.level, self.foldable_message, None, None)

    def title(self, title: str = None) -> None:
        t = title or "Folded Message"
        self.foldable_message += f"<details><summary>{t}</summary>"
        # message += f"{msg}</details>"

    def content(self, msg: str = None, end: bool = False) -> None:
        self.foldable_message += f"{msg}"
        if end:
            self.foldable_message += "</details>"
            self.send_foldable_message()

    def inv_start(self, msg: str = None) -> None:
        self.foldable_message += f"<details><summary>{msg}</summary>"


class FoldableLogHandler(logging.Handler):
    """A handler that only logs DEBUG level messages"""

    def __init__(self, level: int) -> None:
        self.level = level
        super().__init__(level=level)

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno != self.level:
            return
        else:
            print(record.msg)


class FoldableLoggers:
    """
    Custom logger class to add HTML markup to log messages.

    Attributes:
        debug_logger_class: custom class to use for handling debug msgs

    Methods:
        localize(name=__name__, level=logging.WARNING):
            localize the loggers to the current module
        get_loggers():
            return the loggers, ready to use

    Usage:
    >>> from pytest_tui.debug_html_logger import DebugLoggers
    >>> debug_loggers = DebugLoggers()
    >>> debug_loggers.localize(name=__name__, <level=LEVEL>)
    >>> debug_logger = debug_loggers.get_loggers()

    >>> debug_logger.debug(msg)  # should show up as folded in HTML reports
    """

    # def __init__(self):
    #     self.debug_logger_class = DebugLogger

    # def localize(self, name: str=__name__, level: Union[str, int]=logging.DEBUG):
    #     self.debug_logger_class.name = name
    #     self.debug_logger_class.setLevel(10)
    #     self.debug_logger_class.addHandler(DebugLogHandler)

    # def get_logger(self):
    #     logging.setLoggerClass(DebugLogger)
    #     logger = logging.getLogger(logging.getLoggerClass().__name__)
    #     logger.addHandler(DebugLogHandler)

    def __init__(self):
        logging.setLoggerClass(FoldableLogger)
        self.logger = logging.getLogger("FoldableLogger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(FoldableLogHandler())

    def get_debug_logger(self):
        return self.logger
