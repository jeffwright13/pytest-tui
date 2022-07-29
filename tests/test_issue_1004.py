
import pytest

@pytest.fixture
def fixt():
    yield
    raise Exception

def test_foo(fixt):
    pass

def test_foo2(fixt):
    pass

def test_foo3(fixt):
    assert 0

def test_foo4(fixt):
    assert 0
