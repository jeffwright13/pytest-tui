import pytest
import logging
import sys

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
logger.propagate = True
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logging.getLogger("faker").setLevel(logging.ERROR)

# These tests have the same name as in testfile test_1.py
# Used for testing ability to handle duplicate tes names
# across different files


@pytest.fixture
def error_fixture():
    assert 0


def test_a_ok():
    print("This test doesn't have much to say, but it passes - ok!!")


def test_b_fail():
    assert 0


def test_c_error(error_fixture):
    print("This test should be marked as an Error.")
    pass
