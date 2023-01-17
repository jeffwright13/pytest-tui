import random
import time

import pytest

new_outcome = False
outcome = new_outcome


@pytest.mark.flaky(reruns=2)
def test_flaky_1():
    global outcome
    global new_outcome
    new_outcome = True
    assert outcome


new_outcome = False
outcome = new_outcome


@pytest.mark.flaky(reruns=2)
def test_flaky_2():
    global outcome
    global new_outcome
    new_outcome = True
    assert outcome
