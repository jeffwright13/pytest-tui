import logging
import warnings

import pytest

logger = logging.getLogger()


@pytest.mark.xfail()
def test0_xfail():
    print("Test 0 XFail")
    logger.critical("CRITICAL")
    logger.error("ERROR")
    logger.warning("WARNING")
    logger.info("INFO")
    logger.debug("DEBUG")
    warnings.warn(Warning("You ave been warned!"))
    assert False


@pytest.mark.xfail()
def test0_xpass():
    print("Test 0 XPass")
    logger.critical("CRITICAL")
    logger.error("ERROR")
    logger.warning("WARNING")
    logger.info("INFO")
    logger.debug("DEBUG")
    warnings.warn(Warning("You ave been warned!"))
    assert True
