import logging
import random
import warnings

import pytest

logger = logging.getLogger()


@pytest.fixture()
def regex():
    return r"""  *->"""


def test_0_regex_single(regex):
    print("Pre-foldy stuff...")
    print("Test Pass 1!")
    print(regex)
    print("More pre-foldy stuff...")
    print("This line marks the middle of the RegEx fold.")
    print(regex)
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
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
    print("Post-foldy stuff...")
    print("More post-foldy stuff...")
    assert True


def test_0_regex_double(regex):
    print("Pre-foldy stuff...")
    print("Test Pass 1!")
    print(regex)
    print("More pre-foldy stuff...")
    print(f"​​​This line marks the beginning of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print(regex)
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print(regex)
    print("Middle of the foldy stuff...")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print("Middle of the foldy stuff...")
    print("This line marks the middle of the RegEx fold.")
    print("This line marks the middle of the RegEx fold.")
    print(f"￼​This line marks the end of the RegEx fold.")
    print("Post-foldy stuff...")
    print("More post-foldy stuff...")
    assert True
