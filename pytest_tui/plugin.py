import configparser
import itertools
import json
import pickle
import re
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from types import SimpleNamespace

import pytest
import tempfile
from _pytest._io.terminalwriter import TerminalWriter
from _pytest.config import Config, create_terminal_writer
from _pytest.reports import TestReport
from strip_ansi import strip_ansi

from pytest_tui.__main__ import Cli, tui_launch
from pytest_tui.html import main as tuihtml
from pytest_tui.utils import (CONFIGFILE, MARKERS, TERMINAL_OUTPUT_FILE,
                              TUI_RESULT_OBJECTS_FILE, TUI_SECTIONS_FILE,
                              TuiSections, TuiTestResult, TuiTestResults,
                              errors_section_matcher, failures_section_matcher,
                              lastline_matcher, passes_section_matcher,
                              rerun_summary_matcher,
                              short_test_summary_matcher,
                              short_test_summary_test_matcher,
                              test_session_starts_matcher,
                              test_session_starts_test_matcher,
                              warnings_summary_matcher)

# Don't collect tests from any of these files
collect_ignore = [
    "setup.py",
    "plugin.py",
]

# Globals to hold Pytest TestReport instances; and individual test result and
# section objects
_tui_reports = []
_tui_test_results = TuiTestResults()
_tui_sections = TuiSections()
_tui_terminal_out = tempfile.TemporaryFile("wb+")


def pytest_addoption(parser):
    group = parser.getgroup("tui")
    group.addoption(
        "--tui",
        action="store_true",
        help="Enable the pytest-tui plugin. Both text user interface (TUI) and HTML output are supported.",
    )


def add_ansi_to_report(config: Config, report: TestReport):
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


def pytest_report_teststatus(report: TestReport, config: Config):
    """Construct list(s) of individual TestReport instances"""

    if hasattr(report, "caplog") and report.caplog:
        for tui_test_result in _tui_test_results.test_results:
            if tui_test_result.fqtn == report.nodeid:
                tui_test_result.caplog = report.caplog

    if hasattr(report, "capstderr") and report.capstderr:
        for tui_test_result in _tui_test_results.test_results:
            if tui_test_result.fqtn == report.nodeid:
                tui_test_result.capstderr = report.capstderr

    if hasattr(report, "capstdout") and report.capstdout:
        for tui_test_result in _tui_test_results.test_results:
            if tui_test_result.fqtn == report.nodeid:
                tui_test_result.capstdout = report.capstdout

    if hasattr(report, "longreprtext") and report.longreprtext:
        add_ansi_to_report(config, report)
        for tui_test_result in _tui_test_results.test_results:
            if tui_test_result.fqtn == report.nodeid:
                tui_test_result.longreprtext = report.ansi.val

    _tui_reports.append(report)


@pytest.hookimpl()
def pytest_runtest_logstart(nodeid, location):
    for tui_test_result in _tui_test_results.test_results:
        if tui_test_result.fqtn == nodeid:
            tui_test_result.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            break


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    if not hasattr(config.option, "tui"):
        return
    if not config.option.tui:
        return

    config.option.verbose = 1  # easier parsing of final test results
    config.option.reportchars = "A"  # "display all" mode so all results are shown

    # Examine Pytest terminal output to mark different sections of the output.
    # This code is based on the code in pytest's `pastebin.py`.
    tr = config.pluginmanager.getplugin("terminalreporter")
    if tr is not None:

        # Save the old terminal writer instance so we can restore it later
        oldwrite = tr._tw.write

        # identify and mark each results section
        def tee_write(s, **kwargs):
            if re.search(test_session_starts_matcher, s):
                config._tui_current_section = "test_session_starts"
                # _tui_sections.test_session_starts.content += s + "\n"
            if re.search(errors_section_matcher, s):
                config._tui_current_section = "errors"
                # _tui_sections.errors.content += s + "\n"
            if re.search(failures_section_matcher, s):
                config._tui_current_section = "failures"
                # _tui_sections.failures.content += s + "\n"
            if re.search(warnings_summary_matcher, s):
                config._tui_current_section = "warnings_summary"
                # _tui_sections.warnings_summary.content += s + "\n"
            if re.search(passes_section_matcher, s):
                config._tui_current_section = "passes"
                # _tui_sections.passes.content += s + "\n"
            if re.search(rerun_summary_matcher, s):
                config._tui_current_section = "rerun_summary"
                # _tui_sections.rerun_summary.content += s + "\n"
            if re.search(short_test_summary_matcher, s):
                config._tui_current_section = "short_test_summary"
                # _tui_sections.short_test_summary.content += s + "\n"
            if re.search(lastline_matcher, s):
                config._tui_current_section = "lastline"
                _tui_sections.lastline.content += s + "\n"
            else:
                exec(f"_tui_sections.{config._tui_current_section}.content += s")

            # If this is an actual test outcome line in the initial `=== test session starts ==='
            # section, populate the TuiTestResult's fully qualified test name field. Do not add
            # duplicates (as may be encountered with plugins such as pytest-rerunfailures).
            if config._tui_current_section == "test_session_starts" and re.search(
                test_session_starts_test_matcher, s
            ):
                fqtn = re.search(test_session_starts_test_matcher, s)[1]
                if fqtn not in [t.fqtn for t in _tui_test_results.test_results]:
                    _tui_test_results.test_results.append(TuiTestResult(fqtn=fqtn))

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

                for tui_test_result in _tui_test_results.test_results:
                    if tui_test_result.fqtn == fqtn:
                        tui_test_result.outcome = outcome
                        break

            # Write this line's original pytest output text (plus markup) to console.
            # Then markup the line's text by passing it to an instance of TerminalWriter's
            # 'markup' method. (Do not pass "flush" to the method, or it will throw an error
            oldwrite(s, **kwargs)
            s1 = s
            kwargs.pop("flush") if "flush" in kwargs else None
            s1 = TerminalWriter().markup(s, **kwargs)

            # Encode the marked up line so it can be written to the config object.
            # The Pytest config object can be used by plugins for conveying staeful
            # info across an entire test run session.
            # if isinstance(s1, str):
            #     marked_up = s1.encode("utf-8")
            # config._tui_marked += str(marked_up)

            s_orig = s
            kwargs.pop("flush") if "flush" in kwargs else None
            s_orig = TerminalWriter().markup(s, **kwargs)
            if isinstance(s_orig, str):
                unmarked_up = s_orig.encode("utf-8")
            global _tui_terminal_out
            _tui_terminal_out.write(unmarked_up)

        # Write to both terminal/console and tempfiles:
        # _pytui_config._tui_marked, _pytui_config._tui_terminal_out
        tr._tw.write = tee_write


def pytest_unconfigure(config: Config):
    # Populate test result objects with total durations, from each test's TestReport object.
    for tui_test_result, test_report in itertools.product(
        _tui_test_results.test_results, _tui_reports
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
    for tui_test_result in _tui_test_results.test_results:
        if tui_test_result.outcome == "":
            tui_test_result.outcome = "SKIPPED"
            # tui_test_result.duration = 0

    config.pluginmanager.getplugin("terminalreporter")  # <= ???

    # Rewind the temp file containing all the raw ANSI lines sent to the terminal;
    # read its contents;  then close it. Then, write info to file.
    _tui_terminal_out.seek(0)
    terminal_out = _tui_terminal_out.read()
    _tui_terminal_out.close()
    with open(TERMINAL_OUTPUT_FILE, "wb") as file:
        file.write(terminal_out)

    # Pickle the test reult and sections objects to files.
    with open(TUI_RESULT_OBJECTS_FILE, "wb") as file:
        pickle.dump(_tui_test_results, file)
    with open(TUI_SECTIONS_FILE, "wb") as file:
        pickle.dump(_tui_sections, file)

    if hasattr(config.option, "tui") and config.option.tui:
        pytui_tui(config)


def pytui_tui(config: Config) -> None:
    """
    Final code invocation after Pytest run has completed.
    Will call either or both of TUI / HTML code is specified on cmd line.
    """
    config_parser = configparser.ConfigParser()

    # Make sure the config file exists and has section content
    try:
        config_parser.read(CONFIGFILE)
        assert len(config_parser.sections()) > 0
    except Exception:
        Cli().apply_default_config()
    finally:
        config_parser.read(CONFIGFILE)

    try:
        # disable capturing while TUI runs to avoid error `redirected stdin is pseudofile, has
        # no fileno()`; adapted from https://githubmemory.com/repo/jsbueno/terminedia/issues/25
        capmanager = config.pluginmanager.getplugin("capturemanager")
        capmanager.suspend_global_capture(in_=True)
    finally:
        with ThreadPoolExecutor() as executor:
            executor.submit(tuihtml)
        if config_parser["TUI"].get("autolaunch_tui") == "True":
            tui_launch()

        capmanager.resume_global_capture()
