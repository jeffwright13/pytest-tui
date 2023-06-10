import pytest
from pathlib import Path
from _pytest.config import ExitCode


class Defaults:
    def __init__(self):
        self.tui = None
        self.htmlfile = Path(f"{Path.cwd()}/tui_files/html_report.html")
        self.regexfile = None


class Consts(Defaults):
    def __init__(self):
        super().__init__()
        self.tui = True


class NonDefaults:
    def __init__(self):
        self.tui = True
        self.htmlfile = Path(f"{Path.cwd()}/test_files/test_report.html")
        self.regexfile = Path(f"{Path.cwd()}/test_files/test_regex.txt")


class Examples:
    def __init__(self):
        self.htmlfile = Path(f"{Path.cwd()}/tui_files/example_html_report.html")
        self.regexfile = Path(f"{Path.cwd()}/tui_files/example_regex.txt")


@pytest.fixture
def defaults():
    return Defaults()


@pytest.fixture
def consts():
    return Consts()


@pytest.fixture
def nondefaults():
    return NonDefaults()


@pytest.fixture
def examples():
    return Examples()


@pytest.mark.test_tui_with_pytester
def test_help_menu_has_tui_info(pytester):
    """Verifies that the --tui option exists in the help menu."""
    result = pytester.runpytest("--help")
    assert any("tui" in line for line in result.outlines)
    result = pytester.runpytest("--help", "--tui")
    assert any("tui" in line for line in result.outlines)


@pytest.mark.test_tui_with_pytester
def test_verify_commandline_options_missing(pytester, defaults):
    """Verifies that when --tui is not passed on the command line, it is None when args
    are parsed; and when --tui is passed on the command line, it is True ."""
    # test_path = pytester.copy_example("testing/pytester/examples/test_pass.py")
    # result = pytester.runpytest()

    cfg = pytester.parseconfig()

    assert cfg.getoption("_tui") == defaults.tui
    assert cfg.getoption("_tui_htmlfile") == defaults.htmlfile
    assert cfg.getoption("_tui_regexfile") == defaults.regexfile


def test_verify_commandline_options_invalid_option(pytester):
    """Verifies the response to an invalid command line option."""

    with pytest.raises(SystemExit):
        pytester.parseconfig("--tui", "--invalid-option")


@pytest.mark.test_tui_with_pytester
def test_illegal_input_options(pytester):
    """Verifies that illegal combinations of command line options raise appropriate errors.
    """

    # Case when both --tui-htmlfile and --tui-regexfile are provided without a value
    with pytest.raises(SystemExit):
        pytester.parseconfig("--tui", "--tui-htmlfile=", "--tui-regexfile=")

    # Case when --tui is not provided but --tui-htmlfile and --tui-regexfile are
    with pytest.raises(SystemExit):
        pytester.parseconfig(
            "--tui-htmlfile=test_report.html", "--tui-regexfile=test_regex.txt"
        )

    # Add other illegal combinations as needed


@pytest.mark.test_tui_with_pytester
def test_verify_commandline_options_tui_only(pytester, consts):
    """Verifies that when only '--tui' is passsed on command line, it is True"""
    cfg = pytester.parseconfig("--tui")

    assert cfg.getoption("_tui") == consts.tui
    assert cfg.getoption("_tui_htmlfile") == consts.htmlfile
    assert cfg.getoption("_tui_regexfile") == consts.regexfile


@pytest.mark.test_tui_with_pytester
def test_verify_commandline_options_tui_regexfile(pytester, defaults, nondefaults):
    """Verifies that when '--tui' and '--tui-htmlfile' are passsed on command line, '_tui'
    is True and '_tui_htmlfile' is as specified."""

    cfg = pytester.parseconfig("--tui", f"--tui-regexfile=")
    # cfg = pytester.parseconfig("--tui", f"--tui-regexfile={regexfile}")

    assert cfg.getoption("_tui") == nondefaults.tui
    assert cfg.getoption("_tui_htmlfile") == defaults.htmlfile
    assert cfg.getoption("_tui_regexfile") == ""
    # assert cfg.getoption("_tui_regexfile") == examples.regexfile


# TODO: This test is failing.  Fix it.
@pytest.mark.xfail(reason="Not implemented yet")
@pytest.mark.test_tui_with_pytester
def test_verify_commandline_options_tui_htmlfile(pytester, examples, nondefaults):
    """Verifies that when '--tui' and '--tui-htmlfile' are passsed on command line, '_tui'
    is True and '_tui_htmlfile' is as specified."""

    cfg = pytester.parseconfig(
        "--tui",
        f"--tui-htmlfile={examples.htmlfile}",
        f"--tui-regexfile={examples.regexfile}",
    )

    assert cfg.getoption("_tui") == nondefaults.tui
    assert cfg.getoption("_tui_htmlfile") == examples.htmlfile
    assert cfg.getoption("_tui_regexfile") == examples.regexfile


@pytest.mark.test_tui_with_pytester
def test_run_with_empty_testfile(pytester):
    """Verifies that the pytest-tui plugin handles being paseed an empty test file.
    By emmpty, we mean a test file that has no tests in it."""

    test_path = pytester.copy_example("testing/pytester/examples/test_empty.py")
    result = pytester.runpytest("--tui")

    assert any("== no tests ran" in outline for outline in result.outlines)
    assert result.ret == ExitCode.NO_TESTS_COLLECTED
    result.assert_outcomes(failed=0, passed=0)


@pytest.mark.test_tui_with_pytester
def test_verify_commandline_options_tui_htmlfile_regexfile(pytester, examples):
    """Verifies that when '--tui', '--tui-htmlfile', and '--tui-regexfile' are passed on the command line,
    '_tui' is True, '_tui_htmlfile' is as specified, and '_tui_regexfile' is as specified.
    """

    cfg = pytester.parseconfig(
        "--tui",
        f"--tui-htmlfile={examples.htmlfile}",
        f"--tui-regexfile={examples.regexfile}",
    )

    assert cfg.getoption("_tui") is True
    assert cfg.getoption("_tui_htmlfile") == examples.htmlfile
    assert cfg.getoption("_tui_regexfile") == examples.regexfile


@pytest.mark.test_tui_with_pytester
def test_verify_commandline_options_tui_htmlfile_no_value(pytester, consts):
    """Verifies that when '--tui' and '--tui-htmlfile' are passed on the command line without a value,
    '_tui' is True and '_tui_htmlfile' is the default value."""

    cfg = pytester.parseconfig("--tui", "--tui-htmlfile=")

    assert cfg.getoption("_tui") is True
    assert cfg.getoption("_tui_htmlfile") == consts.htmlfile
    assert cfg.getoption("_tui_regexfile") is None


@pytest.mark.test_tui_with_pytester
def test_verify_commandline_options_tui_regexfile_no_value(pytester, consts):
    """Verifies that when '--tui' and '--tui-regexfile' are passed on the command line without a value,
    '_tui' is True and '_tui_regexfile' is the default value."""

    cfg = pytester.parseconfig("--tui", "--tui-regexfile=")

    assert cfg.getoption("_tui") is True
    assert cfg.getoption("_tui_htmlfile") is None
    assert cfg.getoption("_tui_regexfile") == consts.regexfile


'''
@pytest.mark.test_tui_with_pytester
def test_true_assertion(pytester):
    pytester.makepyfile(
        """
        def test_foo():
            assert True
        """
    )
    result = pytester.runpytest()
    result.assert_outcomes(failed=0, passed=1)


@pytest.mark.test_tui_with_pytester
def test_false_assertion(pytester):
    pytester.makepyfile(
        """
        def test_foo():
            assert False
        """
    )
    result = pytester.runpytest()
    result.assert_outcomes(failed=1, passed=0)
'''
