import itertools
import pickle
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Match

from strip_ansi import strip_ansi

# Files generated by plugin.py
PYTEST_TUI_FILES_DIR = Path.cwd() / "pytest_tui_files"
PYTEST_TUI_FILES_DIR.mkdir(exist_ok=True)
HTMLOUTPUTFILE = PYTEST_TUI_FILES_DIR / "html_report.html"
Path(HTMLOUTPUTFILE).touch(exist_ok=True)
CONFIGFILE = PYTEST_TUI_FILES_DIR / "config.ini"
Path(CONFIGFILE).touch(exist_ok=True)
REPORTOBJECTSFILE = PYTEST_TUI_FILES_DIR / "report_objects.bin"
MARKEDTERMINALOUTPUTFILE = PYTEST_TUI_FILES_DIR / "marked_output.bin"
UNMARKEDTERMINALOUTPUTFILE = PYTEST_TUI_FILES_DIR / "unmarked_output.bin"

# regex matching patterns for Pytest sections
test_session_starts_matcher = re.compile(r"^==.*\stest session starts\s==+")
errors_section_matcher = re.compile(r"^==.*\sERRORS\s==+")
failures_section_matcher = re.compile(r"^==.*\sFAILURES\s==+")
warnings_summary_matcher = re.compile(r"^==.*\swarnings summary\s.*==+")
passes_section_matcher = re.compile(r"^==.*\sPASSES\s==+")
rerun_summary_matcher = re.compile(r"^==.*\srerun test summary info\s==+")
short_test_summary_matcher = re.compile(r"^==.*\sshort test summary info\s.*==+")
short_test_summary_test_matcher = re.compile(
    r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+(?:\[\d+\]\s)?(\S+)(?:.*)?$"
)
warnings_summary_test_matcher = re.compile(
    # r"^([^\n]+:{1,2}[^\n]+)\n(([^\n]+)\n)*"
    r"^([^\n]+:{1,2}[^\n]+)\n([^\n]+\n)+"
)
lastline_matcher = re.compile(r"^==.*in\s\d+.\d+s.*=+")
section_name_matcher = re.compile(r"~~>PYTEST_TUI_(\w+)")
standard_test_matcher = re.compile(
    r"(.*\::\S+)\s(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)"
)
live_log_testname_matcher = re.compile(r"(.*::\S+)", re.MULTILINE)
live_log_outcome_matcher = re.compile(
    r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\W.+(\[\W?.*?\])", re.MULTILINE
)

MARKERS = {
    "pytest_tui_test_session_starts": "~~>PYTEST_TUI_TEST_SESSION_STARTS<~~",
    "pytest_tui_errors_section": "~~>PYTEST_TUI_ERRORS_SECTION<~~",
    "pytest_tui_failures_section": "~~>PYTEST_TUI_FAILURES_SECTION<~~",
    "pytest_tui_warnings_summary": "~~>PYTEST_TUI_WARNINGS_SUMMARY<~~",
    "pytest_tui_passes_section": "~~>PYTEST_TUI_PASSES_SECTION<~~",
    "pytest_tui_rerun_summary": "~~>PYTEST_TUI_RERUN_SUMMARY<~~",
    "pytest_tui_short_test_summary": "~~>PYTEST_TUI_SHORT_TEST_SUMMARY<~~",
    "pytest_tui_last_line": "~~>PYTEST_TUI_LAST_LINE<~~",
}


OUTCOMES = (
    "Failures",
    "Passes",
    "Errors",
    "Skipped",
    "Xfails",
    "Xpasses",
)


@dataclass
class SectionInfo:
    """Info relevant to each Pytest output section"""

    name: str = ""
    label: str = ""
    matcher: Match = None
    content: str = r""
    outcome: str = ""


@dataclass
class TestInfo:
    """Info relevant for a single test"""

    nodeid: str = ""
    category: str = ""
    outcome: str = ""
    caplog: str = ""
    capstderr: str = ""
    capstdout: str = ""
    text: str = ""
    keywords: set = ()


class Results:
    """
    This class holds all pertinent information for a given Pytest test run.
    """

    def __init__(self):
        self.reports = []

        self.Sections = self._init_sections()
        self.unmarked_output = self._get_unmarked_output()
        self.marked_output = MarkedSections(self.Sections)
        self.test_results = self._deduplicate_reports()

        self._get_test_outcomes_and_titles()
        self._update_testinfo_text()

        self.Outcomes = self._find_test_outcomes()
        self.tests_errors = self._get_result_by_outcome("ERROR")
        self.tests_failures = self._get_result_by_outcome("FAILED")
        self.tests_passes = self._get_result_by_outcome("PASSED")
        self.tests_skipped = self._get_result_by_outcome("SKIPPED")
        self.tests_xfails = self._get_result_by_outcome("XFAIL")
        self.tests_xpasses = self._get_result_by_outcome("XPASS")

        self.tests_all = {}
        self.tests_all.update(self.tests_errors) if self.tests_errors else None
        self.tests_all.update(self.tests_passes) if self.tests_passes else None
        self.tests_all.update(self.tests_failures) if self.tests_failures else None
        self.tests_all.update(self.tests_skipped) if self.tests_skipped else None
        self.tests_all.update(self.tests_xfails) if self.tests_xfails else None
        self.tests_all.update(self.tests_xpasses) if self.tests_xpasses else None

        self.Warnings = self._find_warnings()

    def _find_warnings(self):
        """
        Find the warning results.
        """
        warnings = {}
        warning_section = self.Sections["WARNINGS_SUMMARY"]
        match = warnings_summary_test_matcher.match(strip_ansi(warning_section.content))
        if match:
            testname = match.group(1)
            warning = match.group(2)
            warnings[testname] = warning
        return warnings

    def _find_test_outcomes(self):
        """
        Find the outcome of each test.
        """
        outcomes = {}
        summary_section = self.Sections["SHORT_TEST_SUMMARY"]
        for line in summary_section.content.splitlines():
            match = short_test_summary_test_matcher.match(strip_ansi(line))
            if match:
                outcome = match.group(1)
                testname = match.group(2)
                outcomes[testname] = outcome
        return outcomes

    def _init_sections(self):
        """
        Initialize SectionInfo dataclass instances"""
        return {
            "TEST_SESSION_STARTS": SectionInfo(
                name="TEST_SESSION_STARTS",
                label="Session Start",
                matcher=test_session_starts_matcher,
            ),
            "ERRORS_SECTION": SectionInfo(
                name="ERRORS_SECTION",
                label="Errors",
                matcher=errors_section_matcher,
                outcome="",
            ),
            "FAILURES_SECTION": SectionInfo(
                name="FAILURES_SECTION",
                label="Failures",
                matcher=failures_section_matcher,
            ),
            "WARNINGS_SUMMARY": SectionInfo(
                name="WARNINGS_SUMMARY",
                label="Warnings",
                matcher=warnings_summary_matcher,
            ),
            "PASSES_SECTION": SectionInfo(
                name="PASSES_SECTION", label="Passes", matcher=passes_section_matcher
            ),
            "RERUN_SUMMARY": SectionInfo(
                name="RERUN_SUMMARY",
                label="Rerun",
                matcher=rerun_summary_matcher,
            ),
            "SHORT_TEST_SUMMARY": SectionInfo(
                name="SHORT_TEST_SUMMARY",
                label="Short Test Summary",
                matcher=short_test_summary_matcher,
            ),
            "LAST_LINE": SectionInfo(
                name="LAST_LINE", label=None, matcher=lastline_matcher
            ),
        }

    def _get_unmarked_output(
        self, unmarked_file_path: Path = UNMARKEDTERMINALOUTPUTFILE
    ) -> list:
        """Get full Pytest terminal output"""
        try:
            with open(unmarked_file_path, "r") as umfile:
                return umfile.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Cannot find {unmarked_file_path}. Have you run pytest with the '--tui' option yet?"
            ) from e

    def _deduplicate_reports(self) -> list:
        """
        Process TestReport objects from Pytest output; remove duplicates;
        extract ANSI-encoded traceback info for failures/passes.
        """
        processed_reports = self._process_reports()
        return list({item.nodeid: item for item in processed_reports}.values())

    def _process_reports(self) -> list:
        """Extract individual test results from full list of Pytest's TestReport instances"""

        test_infos = []
        for report in self._unpickle():
            test_info = TestInfo()
            self.reports.append(report)

            # populate the TestInfo instance with pertinent data from report
            test_info.outcome = report.outcome
            test_info.caplog = report.caplog
            test_info.capstderr = report.capstderr
            test_info.capstdout = report.capstdout
            test_info.nodeid = report.nodeid
            test_info.keywords = set(report.keywords)

            test_infos.append(test_info)
        return test_infos

    def _update_testinfo_text(self):
        for report, test_info in itertools.product(self.reports, self.test_results):
            # for failed test cases, we want the ANSI coded output, not longreprtext;
            # longreprtext has no ANSI codes and all text will be rendered w/o markup
            # if (
            #     test_info.category == "FAILED"
            #     and report.when == "call"
            #     and test_info.nodeid == report.nodeid
            # ):
            #     test_info.text = report.longreprtext
            if hasattr(report, "ansi") and test_info.nodeid == report.nodeid:
                test_info.text = report.ansi.val

    def _update_test_result_by_testname(self, nodeid: str, result: str) -> None:
        for test_result in self.test_results:
            if nodeid == test_result.nodeid:
                test_result.category = result

    def _get_test_outcomes_and_titles(self) -> None:
        """
        Extract test title and outcome from each line of the verbose 'test session starts'
        section. This guarantees that our classification of each test's outcome is the
        same as Pytest's.

        Line formats are different depending on setting of Pytest config option 'log_cli'.
        Hence the two regex matcher flavors (standard / live_log), and the two sections
        of per-line regex analysys (creating a single regex that captures both formats
        reliably was very difficult; hence worked around with with some per-line logic.
        """
        look_for_live_log_outcome = False

        for line in self.Sections["TEST_SESSION_STARTS"].content.split("\n"):
            stripped_line = strip_ansi(line).rstrip()

            # Start out by looking for non-live-log results
            standard_match = re.search(standard_test_matcher, stripped_line)
            if standard_match:
                title = standard_match.groups()[0]
                outcome = standard_match.groups()[1]
                if title and outcome:
                    self._update_test_result_by_testname(title, outcome)
                    title = outcome = None
                continue

            # If the line doesn't match non-live-log format, look for live-log matches;
            # outcomes and testnames in separate searches
            live_log_testname_match = re.search(
                live_log_testname_matcher, stripped_line
            )
            if live_log_testname_match:
                title = live_log_testname_match.groups()[0].strip()
                look_for_live_log_outcome = True
                continue

            live_log_outcome_match = re.search(live_log_outcome_matcher, stripped_line)
            if look_for_live_log_outcome and live_log_outcome_match:
                outcome = live_log_outcome_match.groups()[0].strip()
                look_for_live_log_outcome = False
                self._update_test_result_by_testname(title, outcome)
                title = outcome = None

    def _get_result_by_outcome(self, outcome: str) -> None:
        """Read final `short test summary info` section and extract test outcomes"""
        for test_name, test_outcome in self.Outcomes.items():
            return {
                test_result.nodeid: test_result.text
                + test_result.caplog
                + test_result.capstderr
                + test_result.capstdout
                for test_result in self.test_results
                if test_result.category == outcome
            }

    def _unpickle(self):
        """Unpack pickled Pytest TestReport objects from file"""
        try:
            with open(REPORTOBJECTSFILE, "rb") as rfile:
                return pickle.load(rfile)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Cannot find {REPORTOBJECTSFILE}. Have you run pytest with the '--tui' option yet?"
            ) from e


class MarkedSections:
    """
    This class processes a Pytest output file that has been marked by pytest-tui,
    and identifies its sections. Pytest defines the following possible sections in
    its console output (not all show by default; they are dictated by option settings,
    e.g. in pytest.ini, on cmd line, etc.):
    "=== test session starts ==="
    "=== ERRORS ==="
    "=== FAILURES ==="
    "=== warnings summary ==="
    "=== PASSES ==="
    "=== short test summary info ==="
    "=== rerun test summary info ==="
    "==== failed passed skipped xfailed xpassed warnings errors reruns in 1.23s ==="
    """

    def __init__(
        self, Sections: dict, marked_file_path: Path = MARKEDTERMINALOUTPUTFILE
    ) -> None:
        self.Sections = Sections
        self._marked_lines = self._get_marked_lines(marked_file_path)
        self._sections = self._sectionize(self._marked_lines)
        print("")

    def get_section(self, name: str) -> str:
        # return marked section, or if not found (e.g. didn't occur in output),
        # return blank dict w/ /no section content
        if name in self.Sections:
            return next(
                (section for section in self._sections if name == section.name),
                SectionInfo(),
            )
        else:
            raise NameError(f"Cannot retrieve section by name: '{name}'")

    def _get_marked_lines(
        self, marked_file_path: Path = MARKEDTERMINALOUTPUTFILE
    ) -> list:
        """Return a list of all lines from the marked output file"""
        try:
            with open(MARKEDTERMINALOUTPUTFILE, "r") as mfile:
                return mfile.readlines()
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Cannot find {MARKEDTERMINALOUTPUTFILE}. Have you run pytest with the '--tui' option yet?"
            ) from e

    def _line_is_a_marker(self, line: str) -> bool:
        """Determine if the current line is a marker, or part of Pytest output"""
        return (
            line.strip()
            in (
                MARKERS["pytest_tui_test_session_starts"],
                MARKERS["pytest_tui_errors_section"],
                MARKERS["pytest_tui_failures_section"],
                MARKERS["pytest_tui_passes_section"],
                MARKERS["pytest_tui_warnings_summary"],
                MARKERS["pytest_tui_rerun_summary"],
                MARKERS["pytest_tui_short_test_summary"],
                MARKERS["pytest_tui_last_line"],
            )
            if line.strip()
            else False
        )

    def _sectionize(self, lines: list) -> dict:
        """
        Parse marked lines from test run console output;
        build dictionary of SectionInfo objects
        """
        section_name = ""

        for line in lines:
            if self._line_is_a_marker(line):
                if MARKERS["pytest_tui_last_line"] in line:
                    continue
                section_name = re.search(section_name_matcher, line).groups()[0]
                self.Sections[section_name].content = r""
            elif section_name:
                self.Sections[section_name].content += line
        self.Sections["LAST_LINE"].content = lines[-1]
        return self.Sections
