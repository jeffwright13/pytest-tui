import pytest

@pytest.mark.snowflake
def test_snowflake_1():
    assert True


@pytest.mark.snowflake
def test_snowflake_2():
    assert False
