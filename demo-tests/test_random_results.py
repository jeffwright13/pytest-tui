import logging
import random
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
def random_result_loglevel(faker):
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


def random_result_regex(
    pattern: str, seed: int = 0, num: int = 10, rarity: int = 100
) -> str:
    fake = faker.Faker()
    ret = ""
    random.seed(seed)
    for _ in range(10):
        text = random.choice(
            [f"{fake.sentence()}", f"{fake.paragraph()}", f"{fake.text()}"]
        )
        for j, word in enumerate(text.split(" ")):
            if j % rarity == random.randint(1, rarity):
                ret += f" { pattern }{word} "
            else:
                ret += f" {word}"
    return ret


def test_0():
    logger = logging.get
    logger.info(random_result_regex("  *-> ", 13, 10, 30))
    assert True


def test_1():
    logger = logging.get
    logger.info(random_result_regex("  *-> ", 13, 10, 30))
    assert True
