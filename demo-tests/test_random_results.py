import logging
import random
import warnings
from dataclasses import dataclass

import faker
import pytest

OUTCOMES = [
    "failed",
    "passed",
    "skipped",
    "xfailed",
    "xpassed",
    "warning",
    "error",
    "rerun",
]
WEIGHTS = [0.15, 0.60, 0.05, 0.03, 0.02, 0.07, 0.03, 0.05]

logger = logging.getLogger()


@pytest.fixture
def random_result(faker):
    @dataclass
    class Result:
        outcome: str
        log_msg: str
        log_level: str

    choice = random.choices(OUTCOMES, WEIGHTS)[0]
    if choice == "passed":
        return Result(
            outcome=choice, log_msg=f"Passed: {faker.sentence()}", log_level="info"
        )
    elif choice == "failed":
        return Result(
            outcome=choice, log_msg=f"Failed: {faker.paragraph()}", log_level="error"
        )
    elif choice == "skipped":
        return Result(
            outcome=choice, log_msg=f"Skipped: {faker.sentence()}", log_level="info"
        )
    elif choice == "xfailed":
        return Result(
            outcome=choice, log_msg=f"XFailed: {faker.sentence()}", log_level="info"
        )
    elif choice == "xpassed":
        return Result(
            outcome=choice, log_msg=f"XPassed: {faker.sentence()}", log_level="info"
        )
    elif choice == "warning":
        return Result(
            outcome=choice, log_msg=f"Warning: {faker.sentence()}", log_level="warning"
        )
    elif choice == "error":
        return Result(
            outcome=choice, log_msg=f"Error: {faker.sentence()}", log_level="error"
        )
    elif choice == "rerun":
        return Result(
            outcome=choice, log_msg=f"Rerun: {faker.sentence()}", log_level="info"
        )


def test_0(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_1(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_2(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_3(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_4(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_5(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_6(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_7(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_8(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_9(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)


def test_10(random_result, faker):
    if random_result.outcome == "passed":
        logger.info(random_result.log_msg)
    elif random_result.outcome == "failed":
        logger.error(random_result.log_msg)
        assert False
    elif random_result.outcome == "skipped":
        logger.info(random_result.log_msg)
        pytest.skip(random_result.log_msg)
    elif random_result.outcome == "xfailed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "xpassed":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
    elif random_result.outcome == "warning":
        logger.warning(random_result.log_msg)
        warnings.warn(random_result.log_msg)
    elif random_result.outcome == "error":
        logger.error(random_result.log_msg)
        raise RuntimeError(random_result.log_msg)
    elif random_result.outcome == "rerun":
        logger.info(random_result.log_msg)
        pytest.xfail(random_result.log_msg)
