import logging
import random
import warnings
import time

import pytest


@pytest.mark.timeout(0)
def test_timeout_sleep(logger):
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
