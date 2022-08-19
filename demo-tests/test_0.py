import pytest
import warnings


def test_pass_1():
    print("Test Pass 2!")
    assert True


def test_pass_2():
    print("Test Pass 2!")
    assert True


def test_pass_3():
    print("Test Pass 3!")
    assert True


def test_fail_1():
    print("Test Fail 1!")
    assert False


def test_fail_2():
    print("Test Fail 2!")
    assert False


def test_fail_3():
    print("Test Fail 3!")
    assert False


pytest.mark.skip(reason="Skipping this test with decorator.")
def test_skip():
    assert True


@pytest.mark.xfail()
def test_xfail():
    assert False


@pytest.mark.xfail()
def test_xpass():
    assert True


# Method and its test that causes warnings
def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


def test_warning():
    assert api_v1() == 1
