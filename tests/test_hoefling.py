import pytest


def test_1():
    assert False


def test_2():
    raise RuntimeError("call error")


@pytest.fixture
def f():
    raise RuntimeError("setup error")


def test_3(f):
    assert True


@pytest.fixture
def g():
    yield
    raise RuntimeError("teardown error")


def test_4(g):
    assert True
