import logging
import random
import warnings

import pytest


def test_0_single(logger):
    logger.info(
        "[DETAILS][SUMMARY]Summary of the iteration[/SUMMARY]Verbose logs for iteration"
        " x: ...[/DETAILS]"
    )
    print("Test has run.")
