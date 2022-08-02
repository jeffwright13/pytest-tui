import pytest
import random


@pytest.mark.flaky(reruns=0)
def test_flaky_1():
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=1)
def test_flaky_2():
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=2)
def test_flaky_3():
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=3)
def test_flaky_4():
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=2)
def test_flaky_always_fail():
    assert False


@pytest.mark.flaky(reruns=2)
def test_flaky_always_pass():
    assert True
