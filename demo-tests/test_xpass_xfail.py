import pytest
import faker
import logging
import random
import sys
import warnings

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
logger.propagate = True
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logging.getLogger("faker").setLevel(logging.ERROR)


def test_xfail_by_inline():
    logger.debug("Debug level log line")
    logger.info("info level log line")
    logger.warning("Warning level log line")
    logger.error("Error level log line")
    logger.critical("Critical level log line")
    pytest.xfail("xfailing this test with 'pytest.xfail()'")

    assert False


@pytest.mark.xfail(reason="Here's my reason for xfail: None")
def test_xfail_by_decorator():
    logger.debug("Debug level log line")
    logger.info("info level log line")
    logger.warning("Warning level log line")
    logger.error("Error level log line")
    logger.critical("Critical level log line")

    assert False
