import logging
import random
import warnings
import time

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.timeout(0)
def test_timeout_sleep():
    logger.warning("Sleeping 3...")
    time.sleep(1)
    # logger.warning("Sleeping 3...")
    # time.sleep(1)
    # logger.warning("Sleeping 3...")
    # time.sleep(1)
    # logger.warning("Sleeping 3...")
    # time.sleep(1)
    # logger.warning("Sleeping 3...")
    # time.sleep(1)
    assert True
