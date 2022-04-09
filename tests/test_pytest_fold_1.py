import pytest
import faker
import logging
import random
import sys
import warnings

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
logger.propagate = True
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logging.getLogger("faker").setLevel(logging.ERROR)


@pytest.fixture
def error_fixture():
    assert 0


def test_a_ok():
    print("ok")


def test_b_fail():
    assert 0


def test_c_error(error_fixture):
    pass


def test_d_skip():
    pytest.skip("skipping this test")


def test_e_xfail():
    pytest.xfail("xfailing this test")


@pytest.mark.xfail(reason="always xfail")
def test_f_xpass():
    pass


@pytest.mark.parametrize("test_input, expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_g_eval_parameterized(test_input, expected):
    assert eval(test_input) == expected


@pytest.fixture
def log_testname():
    logger.info(f"Running test {__name__}...")
    logger.info("Setting test up...")
    logger.info("Executing test...")
    # logger.info(faker.Faker().text(random.randint(50, 200)))
    logger.info("Tearing test down...")


def fake_data(min: int = 30, max: int = 120) -> str:
    return faker.Faker().text(random.randint(min, max))


def test_1_passes_and_has_logging_output(log_testname):
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    assert True


def test_2_fails_and_has_logging_output(log_testname):
    logger.critical(fake_data())
    logger.error(fake_data())
    logger.warning(fake_data())
    logger.info(fake_data())
    logger.debug(fake_data())
    assert 0 == 1


def test_3_fails(log_testname):
    assert 0


def test_4_passes(log_testname):
    assert True


@pytest.mark.skip
def test_5_marked_SKIP(log_testname):
    assert 1


@pytest.mark.xfail
def test_6_marked_xfail_but_passes(log_testname):
    assert 1


@pytest.mark.xfail
def test_7_marked_xfail_and_fails(log_testname):
    assert 0


# Method and its test that causes warnings
def api_v1(log_testname):
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


def test_8_causes_a_warning(log_testname):
    assert api_v1() == 1


# # These tests are helpful in showing how pytest deals with various types
# # of output (stdout, stderr, log)
def test_9_lorem_fails(capsys):
    lorem = """"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?

    At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."""
    print(lorem)
    assert False


def test_10_fail_capturing(capsys):
    print("FAIL this stdout is captured")
    print("FAIL this stderr is captured", file=sys.stderr)
    logger.warning("FAIL this log is captured")
    with capsys.disabled():
        print("FAIL stdout not captured, going directly to sys.stdout")
        print("FAIL stderr not captured, going directly to sys.stderr", file=sys.stderr)
        logger.warning("FAIL is this log captured?")
    print("FAIL this stdout is also captured")
    print("FAIL this stderr is also captured", file=sys.stderr)
    logger.warning("FAIL this log is also captured")
    assert False


def test_11_pass_capturing(capsys):
    print("\nPASS this stdout is captured")
    print("PASS this stderr is captured", file=sys.stderr)
    logger.warning("PASS this log is captured")
    with capsys.disabled(log_testname):
        print(
            "PASS stdout not captured (capsys disabled), going directly to sys.stdout"
        )
        print(
            "PASS stderr not captured (capsys disabled), going directly to sys.stderr",
            file=sys.stderr,
        )
        logger.warning("is this log captured?")
    print("PASS this stdout is also captured")
    print("PASS this stderr is also captured", file=sys.stderr)
    logger.warning("PASS this log is also captured")
    assert True


def test_12_fails_and_has_stdout(capsys):
    print("this test fails")
    assert 0 == 1


def test_13_passes_and_has_stdout(capsys):
    print("this test passes")  # stdout is consumed by pytest
    assert True


# These 2 tests can intentionally cause an error - useful for testing output of
# folding - if the fixture is commented out, the test throws an error at setup.
#
# @pytest.fixture()
# def fixture_for_fun(log_testname):
#     pass


def test_14_causes_error_pass_stderr_stdout_stdlog(fixture_for_fun):
    print("PASS this stdout is captured")
    print("PASS this stderr is captured", file=sys.stderr)
    logger.warning("PASS this log is captured")
    assert 1


def test_15_causes_error_fail_stderr_stdout_stdlog(fixture_for_fun):
    print("FAIL this stdout is captured")
    print("FAIL this stderr is captured", file=sys.stderr)
    logger.warning("FAIL this log is captured")
    assert 0
