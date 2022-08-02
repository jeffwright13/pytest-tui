import pytest


@pytest.fixture
def bad():
    yield
    raise Exception


def test_foo(bad):
    assert True


def test_foo2(bad):
    assert False


@pytest.fixture
def good():
    yield
    pass


def test_foo(good):
    assert True


def test_foo2(good):
    assert False
