import logging
import random
import warnings

import pytest

logger = logging.getLogger()


def test_0_single():
    logger.info(
        "[DETAILS][SUMMARY]Summary of the iteration[/SUMMARY]Verbose logs for iteration"
        " x: ...[/DETAILS]"
    )
    print("Test has run.")
