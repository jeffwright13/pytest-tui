import logging
import random
import warnings

import pytest

logger = logging.getLogger()


# 3 consecutive ZWS
ZWS_X3 = r"""​​​"""
# 1 BOM followed by 1 ZWS
BOM_ZWS = r"""￼​"""
# 3 consecutive ZWJ
ZWJ_X3 = r"""‍‍‍"""
# 1 BOM followed by 1 ZWJ
BOM_ZWJ = r"""￼‍"""


def test0_10_fail_capturing(capsys):
    logger.info(ZWS_X3)
    print("FAIL this stdout is captured")
    print("FAIL this stderr is captured", file=sys.stderr)
    logger.warning("FAIL this log is captured")
    with capsys.disabled():
        print("FAIL stdout not captured, going directly to sys.stdout")
        print("FAIL stderr not captured, going directly to sys.stderr", file=sys.stderr)
        logger.warning("FAIL is this log captured?")
    print("FAIL this stdout is also captured")
    print("FAIL this stderr is also captured", file=sys.stderr)
    logger.warning("FAIL this log is also captured")
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    logger.info(ZWJ_X3)
    assert False


def test0_pass_1():
    print("Test Pass 1!")
    logger.info(ZWS_X3)
    logger.critical("CRITICAL")
    logger.error("ERROR")
    logger.warning("WARNING")
    logger.info("INFO")
    logger.debug("DEBUG")
    logger.info(ZWJ_X3)
    assert True


def test0_pass_2_logs():
    print("Test Pass 2!")
    logger.info(ZWS_X3)
    logger.critical("CRITICAL")
    logger.error("ERROR")
    logger.warning("WARNING")
    logger.info("INFO")
    logger.debug("DEBUG")
    logger.info(ZWJ_X3)
    assert True


@pytest.fixture
def error_fixt():
    raise Exception("Error in fixture")


def test0_pass_3_error_in_fixture(error_fixt):
    print("Test Pass 3!")
    assert True


def test0_fail_1():
    print("Test Fail 1!")
    assert 1 == 2


pytest.mark.skip(reason="Skipping this test with decorator.")


def test0_skip():
    assert True


@pytest.mark.xfail()
def test0_xfail():
    print("Test 0 XFail")
    logger.info(ZWS_X3)
    logger.critical("CRITICAL")
    logger.error("ERROR")
    logger.warning("WARNING")
    logger.info("INFO")
    logger.debug("DEBUG")
    logger.info(ZWJ_X3)
    assert False


@pytest.mark.xfail()
def test0_xpass():
    print("Test 0 XPass")
    logger.info(ZWS_X3)
    logger.critical("CRITICAL")
    logger.error("ERROR")
    logger.warning("WARNING")
    logger.info("INFO")
    logger.debug("DEBUG")
    logger.info(ZWJ_X3)
    assert True


# Method and its test that causes warnings
def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


def test0_warning():
    assert api_v1() == 1


@pytest.mark.flaky(reruns=5)
def test_flaky_3():
    assert random.choice([True, False])
