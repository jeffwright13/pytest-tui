import pytest


@pytest.fixture
def error_fixt():
    raise Exception("Error in fixture")


def test0_pass_3_error_in_fixture(error_fixt):
    print("Test Pass 3!")
    assert True
