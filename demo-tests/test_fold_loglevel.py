import logging
import random
import warnings

import pytest

from typing import Literal

logger = logging.getLogger()

from pytest_tui.utils import TUI_FOLD_TITLE_BEGIN, TUI_FOLD_TITLE_END


def log_output(level):
    exec(f'logger.{level}("Pre-foldy stuff...")')
    exec(f'logger.{level}("More pre-foldy stuff...")')
    print(f"{TUI_FOLD_TITLE_BEGIN}This line marks the beginning of the RegEx fold.")
    exec(f'logger.{level}("This line is in the middle of the RegEx fold.")')
    exec(f'logger.{level}("This line is in the middle of the RegEx fold.")')
    exec(f'logger.{level}("This line is in the middle of the RegEx fold.")')
    exec(f'logger.{level}("This line is in the middle of the RegEx fold.")')
    exec(f'logger.{level}("Middle of the foldy stuff...")')
    exec(f'logger.{level}("This line is in the middle of the RegEx fold.")')
    exec(f'logger.{level}("This line is in the middle of the RegEx fold.")')
    exec(f'logger.{level}("This line is in the middle of the RegEx fold.")')
    print(f"This line marks the end of the RegEx fold.{TUI_FOLD_TITLE_END}")
    exec(f'logger.{level}("Post-foldy stuff...")')
    exec(f'logger.{level}("More post-foldy stuff...")')


@pytest.mark.parametrize(
    "level",
    ["debug", "info", "warning", "error", "critical"],
)
def test_logfold_log_levels(
    level: Literal["debug", "info", "warning", "error", "critical"]
):
    for _ in range(10):
        exec(f"logger.{level}('This is a {level} message.')")
        exec("logger.debug('This is a debug message.')")
        exec("logger.info('This is an info message.')")
        exec("logger.warning('This is a warning message.')")
        exec("logger.error('This is an error message.')")
        exec("logger.critical('This is a critical message.')")
    assert True


@pytest.mark.parametrize(
    "level",
    ["debug", "info", "warning", "error", "critical"],
)
def test_logfold_pass(level: Literal["debug", "info", "warning", "error", "critical"]):
    log_output(level)
    assert True


def test_logfold_fail(level: Literal["debug", "info", "warning", "error", "critical"]):
    log_output(level)
    assert False


def test_logfold_xfail(level: Literal["debug", "info", "warning", "error", "critical"]):
    log_output(level)
    pytest.xfail("XFail")
    assert False


def test_logfold_xpass(level: Literal["debug", "info", "warning", "error", "critical"]):
    log_output(level)
    pytest.xfail("XPass")
    assert True


def test_logfold_skip(level: Literal["debug", "info", "warning", "error", "critical"]):
    log_output(level)
    pytest.skip("Skip")
    assert False


def test_logfold_skipif_true(
    level: Literal["debug", "info", "warning", "error", "critical"]
):
    log_output(level)
    pytest.skipif(True, "SkipIf True")
    assert True


def test_logfold_skipif_false(
    level: Literal["debug", "info", "warning", "error", "critical"]
):
    log_output(level)
    pytest.skipif(False, "SkipIf False")
    assert False


def test_logfold_skipif_true_but_false(
    level: Literal["debug", "info", "warning", "error", "critical"]
):
    log_output(level)
    pytest.skipif(True, "SkipIf True")
    assert False


def test_logfold_skipif_false_but_true(
    level: Literal["debug", "info", "warning", "error", "critical"]
):
    log_output(level)
    pytest.skipif(False, "SkipIf False")
    assert True
