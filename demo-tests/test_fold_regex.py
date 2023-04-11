import logging
import random
import warnings

import pytest

logger = logging.getLogger()

# 3 consecutive ZWS
TUI_FOLD_TITLE_BEGIN = r"""​​​"""
# 1 BOM followed by 1 ZWS
TUI_FOLD_TITLE_END = r"""￼​"""
regex_start_marker = TUI_FOLD_TITLE_BEGIN
regex_end_marker = TUI_FOLD_TITLE_END


def test0_pass_1():
    print("Pre-foldy stuff...")
    print("Test Pass 1!")
    print("More pre-foldy stuff...")
    print(f"{TUI_FOLD_TITLE_BEGIN}This line marks the beginning of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("Middle of the foldy stuff...")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("Middle of the foldy stuff...")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("Middle of the foldy stuff...")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("Middle of the foldy stuff...")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print(f"This line marks the end of the RegEx fold.{TUI_FOLD_TITLE_END}")
    print("Post-foldy stuff...")
    print("More post-foldy stuff...")
    assert True
