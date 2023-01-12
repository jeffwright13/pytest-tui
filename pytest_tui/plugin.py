import itertools
import pickle
import re
import tempfile

# from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from io import StringIO
from types import SimpleNamespace

import pytest
from _pytest._io.terminalwriter import TerminalWriter
from _pytest.config import Config, create_terminal_writer
from _pytest.reports import TestReport
from strip_ansi import strip_ansi

# from pytest_tui.__main__ import tui_launch
# from pytest_tui.html import main as tuihtml
from pytest_tui.utils import (
    TERMINAL_OUTPUT_FILE,
    TUI_RESULT_OBJECTS_FILE,
    TUI_SECTIONS_FILE,
    TuiSections,
    TuiTestResult,
    TuiTestResults,
    errors_section_matcher,
    failures_section_matcher,
    lastline_matcher,
    passes_section_matcher,
    short_test_summary_matcher,
    short_test_summary_test_matcher,
    test_session_starts_matcher,
    test_session_starts_test_matcher,
    warnings_summary_matcher,
)

# Don't collect tests from any of these files
collect_ignore = [
    "setup.py",
    "plugin.py",
]


def pytest_addoption(parser) -> None:
    group = parser.getgroup("tui")
    group.addoption(
        "--tui",
        action="store_true",
        help="Enable the pytest-tui plugin. Both text user interface (TUI) and HTML output are supported.\nRun TUI with console command 'tui'; run HTML report with 'tuih'.",
    )


def add_ansi_to_report(config: Config, report: TestReport) -> None:
    """
    If the report has longreprtext (traceback info), mark it up with ANSI codes
    From https://stackoverflow.com/questions/71846269/algorithm-for-extracting-first-and-last-lines-from-sectionalized-output-file
    """
    buf = StringIO()
    buf.isatty = lambda: True

    reporter = config.pluginmanager.getplugin("terminalreporter")
    original_writer = reporter._tw
    writer = create_terminal_writer(config, file=buf)
    reporter._tw = writer

    reporter._outrep_summary(report)
    buf.seek(0)
    ansi = buf.read()
    buf.close()

    report.ansi = SimpleNamespace()
    setattr(report.ansi, "val", ansi)

    reporter._tw = original_writer


def pytest_cmdline_main(config: Config) -> None:
    # Set up the TUI-specific attributes on the config object:
    # Verbose (easier parsing of final test results)
    # Reportchars =RA (all test results, plus Reruns)
    if hasattr(config.option, "tui"):
        if config.option.tui:
            config.option.verbose = 1
            config.option.reportchars = "A"
        if hasattr(config.option, "reruns"):
            config.option.reportchars = "AR"


def pytest_report_teststatus(report: TestReport, config: Config) -> None:
    # Don't process any TUI-specific code if the plugin is not enabled
    if not hasattr(config.option, "tui"):
        return
    if not config.option.tui:
        return

    if hasattr(report, "caplog") and report.caplog:
        for tui_test_result in config._tui_test_results.test_results:
            if tui_test_result.fqtn == report.nodeid:
                tui_test_result.caplog = report.caplog

    if hasattr(report, "capstderr") and report.capstderr:
        for tui_test_result in config._tui_test_results.test_results:
            if tui_test_result.fqtn == report.nodeid:
                tui_test_result.capstderr = report.capstderr

    if hasattr(report, "capstdout") and report.capstdout:
        for tui_test_result in config._tui_test_results.test_results:
            if tui_test_result.fqtn == report.nodeid:
                tui_test_result.capstdout = report.capstdout

    if hasattr(report, "longreprtext") and report.longreprtext:
        add_ansi_to_report(config, report)
        for tui_test_result in config._tui_test_results.test_results:
            if tui_test_result.fqtn == report.nodeid:
                tui_test_result.longreprtext = report.ansi.val

    config._tui_reports.append(report)


@pytest.hookimpl()
def pytest_runtest_setup(item):
    # Don't process any TUI-specific code if the plugin is not enabled
    if not hasattr(item.config.option, "tui"):
        return
    if not item.config.option.tui:
        return

    for tui_test_result in item.config._tui_test_results.test_results:
        if tui_test_result.fqtn == item.nodeid:
            tui_test_result.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            break


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    # Don't process any TUI-specific code if the plugin is not enabled
    if not hasattr(config.option, "tui"):
        return
    if not config.option.tui:
        return

    # Initialize Config object items to use throughout rest of test session.
    # Ideally these would be init'd earlier in the pytest protocol, but it was found that some
    # custom implementations of pytest frameworks will call pytest.configure() BEFORE other hooks
    # (like pytest_sessionstart or pytest_load_initial_conftests), so we need to init here.
    if not hasattr(config, "_tui_sessionstart"):
        config._tui_sessionstart = True
    if not hasattr(config, "_tui_current_section"):
        config._tui_current_section = "pre_test"
    if not hasattr(config, "_tui_reports"):
        config._tui_reports = []
    if not hasattr(config, "_tui_test_results"):
        config._tui_test_results = TuiTestResults()
    if not hasattr(config, "_tui_sections"):
        config._tui_sections = TuiSections()
    if not hasattr(config, "_tui_terminal_out"):
        config._tui_terminal_out = tempfile.TemporaryFile("wb+")

    # Examine Pytest terminal output to mark different sections of the output.
    # This code is based on the code in pytest's `pastebin.py`.
    tr = config.pluginmanager.getplugin("terminalreporter")
    if tr is not None:

        # Save the old terminal writer instance so we can restore it later
        oldwrite = tr._tw.write

        # identify and mark each results section
        def tee_write(s, **kwargs):

            # Check to see if current line is a section start marker
            if re.search(test_session_starts_matcher, s):
                config._tui_current_section = "test_session_starts"
            if re.search(errors_section_matcher, s):
                config._tui_current_section = "errors"
            if re.search(failures_section_matcher, s):
                config._tui_current_section = "failures"
            if re.search(warnings_summary_matcher, s):
                config._tui_current_section = "warnings_summary"
            if re.search(passes_section_matcher, s):
                config._tui_current_section = "passes"
            if re.search(short_test_summary_matcher, s):
                config._tui_current_section = "short_test_summary"
            if re.search(lastline_matcher, s):
                config._tui_current_section = "lastline"
            else:
                # This line is not a section start marker
                if config._tui_sessionstart:
                    config._tui_current_section = "test_session_starts"
                    config._tui_sessionstart = False

            # If this is an actual test outcome line in the initial `=== test session starts ==='
            # section, populate the TuiTestResult's fully qualified test name field. Do not add
            # duplicates (as may be encountered with plugins such as pytest-rerunfailures).
            if config._tui_current_section == "test_session_starts" and re.search(
                test_session_starts_test_matcher, s
            ):
                fqtn = re.search(test_session_starts_test_matcher, s)[1]
                if fqtn not in [t.fqtn for t in config._tui_test_results.test_results]:
                    config._tui_test_results.test_results.append(
                        TuiTestResult(fqtn=fqtn)
                    )

            # If this is an actual test outcome line in the `=== short test summary info ===' section,
            # populate the TuiTestResult's outcome field.
            if config._tui_current_section == "short_test_summary" and re.search(
                short_test_summary_test_matcher, strip_ansi(s)
            ):

                outcome = re.search(
                    short_test_summary_test_matcher, strip_ansi(s)
                ).groups()[0]
                fqtn = re.search(
                    short_test_summary_test_matcher, strip_ansi(s)
                ).groups()[1]

                for tui_test_result in config._tui_test_results.test_results:
                    if tui_test_result.fqtn == fqtn:
                        tui_test_result.outcome = outcome
                        break

            # Write this line's original pytest output text (plus markup) to console.
            # Also write marked up content to this TUISection's 'content' field.
            # Markup is done w/ TerminalWriter's 'markup' method.
            # (do not pass "flush" to the method, or it will throw an error)
            oldwrite(s, **kwargs)
            kwargs.pop("flush") if "flush" in kwargs else None

            s_orig = s
            kwargs.pop("flush") if "flush" in kwargs else None
            s_orig = TerminalWriter().markup(s, **kwargs)
            exec(
                f"config._tui_sections.{config._tui_current_section}.content += s_orig"
            )
            if isinstance(s_orig, str):
                unmarked_up = s_orig.encode("utf-8")
            config._tui_terminal_out.write(unmarked_up)

        # Write to both terminal/console and tempfiles
        tr._tw.write = tee_write


def pytest_unconfigure(config: Config) -> None:
    # Don't process any TUI-specific code if the plugin is not enabled
    if not hasattr(config.option, "tui"):
        return
    if not config.option.tui:
        return

    # Populate test result objects with total durations, from each test's TestReport object.
    for tui_test_result, test_report in itertools.product(
        config._tui_test_results.test_results, config._tui_reports
    ):
        if test_report.nodeid == tui_test_result.fqtn:
            tui_test_result.duration += test_report.duration

    # Assume any test that was not categorized earlier with an outcome is a Skipped test.
    # JUSTIFICATION:
    # Pytest displays Skipped tests in a different format than all other test categories in the
    # "=== short test summary info ===" section, truncating their fqtns and appending a line number
    # instead of specifying their test names. This plugin identifies all other test categories
    # (passed, failed, errors, etc.) and populates their fqtns and outcomes with the appropriate
    # values, leaving open one other possibility (Skipped).
    for tui_test_result in config._tui_test_results.test_results:
        if tui_test_result.outcome == "":
            tui_test_result.outcome = "SKIPPED"

    config.pluginmanager.getplugin("terminalreporter")  # <= ???

    # Rewind the temp file containing all the raw ANSI lines sent to the terminal;
    # read its contents;  then close it. Then, write info to file.
    config._tui_terminal_out.seek(0)
    terminal_out = config._tui_terminal_out.read()
    config._tui_terminal_out.close()
    with open(TERMINAL_OUTPUT_FILE, "wb") as file:
        file.write(terminal_out)

    with open(TUI_RESULT_OBJECTS_FILE, "wb") as file:
        pickle.dump(config._tui_test_results, file)
    with open(TUI_SECTIONS_FILE, "wb") as file:
        pickle.dump(config._tui_sections, file)
    pytui_launch(config)


def pytui_launch(config: Config) -> None:
    """
    Final code invocation after Pytest run has completed.
    """
    try:
        # disable capturing while TUI runs to avoid error `redirected stdin is pseudofile, has
        # no fileno()`; adapted from https://githubmemory.com/repo/jsbueno/terminedia/issues/25
        capmanager = config.pluginmanager.getplugin("capturemanager")
        capmanager.suspend_global_capture(in_=True)
    finally:
        # re-enable capturing
        # with ThreadPoolExecutor() as executor:
        #     executor.submit(tuihtml)
        # tui_launch()
        capmanager.resume_global_capture()
