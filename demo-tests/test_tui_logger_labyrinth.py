import logging
import math
import random
from logging import DEBUG, ERROR, INFO, WARNING, getLogger

import faker
from rich import inspect

from pytest_tui.data import fake_data
from pytest_tui.tui_logger import (
    ContentBeginLogger,
    ContentEndLogger,
    ContentLogger,
    TitleLogger,
)
from pytest_tui.utils import (
    TUI_FOLD_CONTENT_BEGIN,
    TUI_FOLD_CONTENT_END,
    TUI_FOLD_TITLE_BEGIN,
    TUI_FOLD_TITLE_END,
)

logger = getLogger("StandardPythonLogger")
title_logger = TitleLogger("TitleLogger")
content_begin_logger = ContentBeginLogger("ContentBeginLogger")
content_logger = ContentLogger("ContentLogger")
content_end_logger = ContentEndLogger("ContentEndLogger")


def func_d():
    content_begin_logger.warning("Initial log entry from func_d")
    content_logger.warning(fake_data())
    result = math.sqrt(4)
    logging.info(f"Function D completed. Result: {result}")
    content_logger.warning(fake_data())
    content_end_logger.warning("End log entry from func_d")
    return result


class MyClass:
    def __init__(self, x):
        self.x = x
        logging.info(f"Class MyClass created with x = {self.x}")

    def func_c(self):
        title_logger.warning("Click into me to see All The Logs level c!")
        logging.info("Starting function C")
        content_begin_logger.warning("Initial log entry from func_c")
        content_logger.warning(fake_data())
        result = math.pow(self.x, 2)
        content_end_logger.warning("End log entry from func_c")
        content_logger.warning(fake_data())
        logging.info(f"Function C completed. Result: {result}")
        return result

    class InnerClass:
        def __init__(self, y):
            self.y = y
            logging.info(f"InnerClass created with y = {self.y}")

        def func_b(self):
            title_logger.warning("Click into me to see All The Logs level b!")
            logging.info("Starting function B")
            content_begin_logger.warning("Initial log entry from func_b")
            content_logger.warning(fake_data())
            result = math.cos(self.y)
            content_logger.warning(fake_data())
            content_end_logger.warning("End log entry from func_b")
            logging.info(f"Function B completed. Result: {result}")
            return result

        class InnerInnerClass:
            def __init__(self, z):
                self.z = z
                logging.info(f"InnerInnerClass created with z = {self.z}")

            def func_a(self):
                title_logger.warning("Click into me to see All The Logs level a!")
                logging.info("Starting function A")
                content_begin_logger.warning("Initial log entry from func_a")
                content_logger.warning(fake_data())
                result = math.sin(self.z)
                content_end_logger.warning("End log entry from func_a")
                logging.info(f"Function A completed. Result: {result}")
                return result


def test_labyrinth():
    title_logger.warning("Click into me to see All The Logs!")
    content_begin_logger.warning("Initial log entry from nested_outer_function")
    my_class = MyClass(3)
    inner_class = my_class.InnerClass(1)
    inner_inner_class = inner_class.InnerInnerClass(2)
    result_a = inner_inner_class.func_a()
    result_b = inner_class.func_b()
    result_c = my_class.func_c()
    result_d = func_d()
    content_end_logger.warning("Final log entry from nested_outer_function")
    logging.info("Program completed")
    assert True
