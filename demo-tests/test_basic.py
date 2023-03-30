import logging
import random
import warnings

import pytest

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def test_basic_pass_1(fake_data):
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    assert True


@pytest.fixture
def error_fixt(fake_data):
    raise Exception("Error in fixture")


def test_basic_pass_3_error_in_fixture(error_fixt):
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    assert True


def test_basic_fail_1(fake_data):
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    assert 1 == 2


pytest.mark.skip(reason="Skipping this test with decorator.")


def test_basic_skip(fake_data):
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    assert True


@pytest.mark.xfail()
def test_basic_xfail(fake_data):
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    assert False


@pytest.mark.xfail()
def test_basic_xpass(fake_data):
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    logger.debug(fake_data)
    assert True


# Method and its test that causes warnings
def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


def test_basic_warning():
    assert api_v1() == 1
