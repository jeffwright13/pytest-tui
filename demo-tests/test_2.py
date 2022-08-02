import faker
import pytest
import logging
import random
import sys

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
logger.propagate = True
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logging.getLogger("faker").setLevel(logging.DEBUG)

# These tests have the same name as in testfile test_1.py
# Used for testing ability to handle duplicate tes names
# across different files


def fake_data(min: int = 300, max: int = 600) -> str:
    return faker.Faker().text(random.randint(min, max))


@pytest.fixture
def error_fixture():
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    assert 0


def test_a_ok():
    print("This test doesn't have much to say, but it passes - ok!!")
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())


def test_b_fail():
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    assert 0


def test_c_error(error_fixture):
    print("This test should be marked as an Error.")
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    pass


def test_d1_skip():
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    pytest.skip("Skipping this test with inline call to 'pytest.skip()'.")


pytest.mark.skip(reason="Skipping this test with decorator.")


def test_d2_skip():
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())


def test_d3_skip():
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    pytest.skip("Skipping this test with inline call to 'pytest.skip()'.")


def test_e1():
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())


@pytest.mark.xfail(reason="Marked as Xfail with decorator.")
def test_e2():
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())


def test_f1():
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    assert True
