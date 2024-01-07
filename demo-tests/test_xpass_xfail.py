import logging
import random
import sys
import warnings

import faker
import pytest

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def test_xfail_by_inline(logger):
    logger.debug("Debug level log line")
    logger.info("info level log line")
    logger.warning("Warning level log line")
    logger.error("Error level log line")
    logger.critical("Critical level log line")
    pytest.xfail("xfailing this test with 'pytest.xfail()'")

    assert False


@pytest.mark.xfail(reason="Here's my reason for xfail: None")
def test_xfail_by_decorator(logger):
    logger.debug("Debug level log line")
    logger.info("info level log line")
    logger.warning("Warning level log line")
    logger.error("Error level log line")
    logger.critical("Critical level log line")

    assert False
