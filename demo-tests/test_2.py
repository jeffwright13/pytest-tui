import pytest

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

# These tests have the same name as in testfile test_1.py
# Used for testing ability to handle duplicate test names
# across different files


@pytest.fixture
def error_fixture(fake_data, logger):
    logger.critical(fake_data)
    logger.error(fake_data)
    logger.warning(fake_data)
    logger.info(fake_data)
    logger.debug(fake_data)
    assert 0


def test_a_ok(fake_data, logger):
    print("This test doesn't have much to say, but it passes - ok!!")
    logger.critical(fake_data)
    logger.error(fake_data)
    logger.warning(fake_data)
    logger.info(fake_data)
    logger.debug(fake_data)


def test_b_fail(fake_data, logger):
    logger.critical(fake_data)
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    assert 0


def test_c_error(fake_data, error_fixture, logger):
    print("This test should be marked as an Error.")
    logger.critical(fake_data)
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    pass


def test_d1_skip(fake_data, logger):
    logger.critical(fake_data)
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    pytest.skip("Skipping this test with inline call to 'pytest.skip()'.")


pytest.mark.skip(reason="Skipping this test with decorator.")


def test_d2_skip(fake_data, logger):
    logger.critical(fake_data)
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())


def test_d3_skip(fake_data, logger):
    logger.critical(fake_data)
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    pytest.skip("Skipping this test with inline call to 'pytest.skip()'.")


def test_e1(fake_data, logger):
    logger.critical(fake_data)
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())


@pytest.mark.xfail(reason="Marked as Xfail with decorator.")
def test_e2(fake_data, logger):
    logger.critical(fake_data)
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())


def test_f1(fake_data, logger):
    logger.critical(fake_data)
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    assert True
