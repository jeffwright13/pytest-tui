import random
import time

import pytest


@pytest.mark.flaky(reruns=0)
def test_flaky_0():
    time.sleep(random.uniform(0.1, 0.75))
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=1)
def test_flaky_1():
    time.sleep(random.uniform(0.1, 0.75))
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=2)
def test_flaky_2():
    time.sleep(random.uniform(0.1, 0.75))
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=3)
def test_flaky_3():
    time.sleep(random.uniform(0.1, 0.75))
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=2)
def test_flaky_always_fail():
    time.sleep(random.uniform(0.1, 0.75))
    assert False


@pytest.mark.flaky(reruns=2)
def test_flaky_always_pass():
    time.sleep(random.uniform(0.1, 0.75))
    assert True
