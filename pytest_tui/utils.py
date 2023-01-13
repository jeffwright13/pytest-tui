import pickle
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List

# Files generated by plugin.py
PYTEST_TUI_FILES_DIR = Path.cwd().resolve() / "ptt_files"
PYTEST_TUI_FILES_DIR.mkdir(exist_ok=True)
HTML_OUTPUT_FILE = PYTEST_TUI_FILES_DIR / "html_report.html"
Path(HTML_OUTPUT_FILE).touch(exist_ok=True)
# CONFIGFILE = PYTEST_TUI_FILES_DIR / "config.ini"
# Path(CONFIGFILE).touch(exist_ok=True)
TUI_RESULTS_FILE = PYTEST_TUI_FILES_DIR / "tui_results.pickle"
TUI_RESULT_OBJECTS_FILE = PYTEST_TUI_FILES_DIR / "tui_result_objects.pickle"
TUI_SECTIONS_FILE = PYTEST_TUI_FILES_DIR / "tui_sections.pickle"
TERMINAL_OUTPUT_FILE = PYTEST_TUI_FILES_DIR / "terminal_output.ansi"

# regex matching patterns for Pytest sections
# live_log_sessionstart_matcher = re.compile(r"^==.*\s live log sessionstart\s==+")
test_session_starts_matcher = re.compile(r"^==.*\stest session starts\s==+")
test_session_starts_test_matcher = re.compile(r"^(.*\::\S+)\s")
errors_section_matcher = re.compile(r"^==.*\sERRORS\s==+")
failures_section_matcher = re.compile(r"^==.*\sFAILURES\s==+")
warnings_summary_matcher = re.compile(r"^==.*\swarnings summary\s.*==+")
passes_section_matcher = re.compile(r"^==.*\sPASSES\s==+")
short_test_summary_matcher = re.compile(r"^==.*\sshort test summary info\s.*==+")
short_test_summary_test_matcher = re.compile(
    r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+(?:\[\d+\]\s)?(\S+)(?:.*)?$"
)
warnings_summary_test_matcher = re.compile(r"^([^\n]+:{1,2}[^\n]+)\n([^\n]+\n)+")
lastline_matcher = re.compile(r"^==.*in\s\d+.\d+s.*=+")
section_name_matcher = re.compile(r"~~>PYTEST_TUI_(\w+)")
standard_test_matcher = re.compile(
    r"(.*\::\S+)\s(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)"
)


OUTCOMES = (
    "Failures",
    "Passes",
    "Errors",
    "Skipped",
    "Xfails",
    "Xpasses",
)


@dataclass
class TuiTestResult:
    fqtn: str = ""
    outcome: str = ""
    start_time: datetime = None
    duration: float = 0.0
    caplog: str = ""
    capstderr: str = ""
    capstdout: str = ""
    longreprtext: str = ""

    @staticmethod
    def categories():
        return [
            "fqtn",
            "outcome",
            "start_time",
            "duration",
            "caplog",
            "capstderr",
            "capstdout",
            "longreprtext",
        ]

    def to_list(self):
        return [
            self.fqtn,
            self.outcome,
            self.start_time,
            self.duration,
            self.caplog,
            self.capstderr,
            self.capstdout,
            self.longreprtext,
        ]

    def to_dict(self):
        return {
            "fqtn": self.fqtn,
            "outcome": self.outcome,
            "start_time": self.start_time,
            "duration": self.duration,
            "caplog": self.caplog,
            "capstderr": self.capstderr,
            "capstdout": self.capstdout,
            "longreprtext": self.longreprtext,
        }


@dataclass
class TuiTestResults:
    test_results: List[TuiTestResult] = field(default_factory=list)

    @staticmethod
    def categories():
        return TuiTestResult.categories()

    def to_list(self):
        return list(self.test_results)

    def to_dict(self):
        return {test_result.fqtn: test_result for test_result in self.test_results}

    def to_dict_dict(self):
        return {
            test_result.fqtn: test_result.to_dict() for test_result in self.test_results
        }

    def all_by_time(self):
        return sorted(self.test_results, key=lambda x: x.start_time)

    def all_by_fqtn(self):
        return sorted(self.test_results, key=lambda x: x.fqtn)

    def all_by_outcome(self):
        return sorted(self.test_results, key=lambda x: x.outcome)

    def all_by_outcome_then_time(self):
        return sorted(self.test_results, key=lambda x: (x.outcome, x.start_time))

    def all_tests(self):
        return list(self.test_results)

    def all_failures(self):
        return [
            test_result
            for test_result in self.test_results
            if test_result.outcome == "FAILED"
        ]

    def all_passes(self):
        return [
            test_result
            for test_result in self.test_results
            if test_result.outcome == "PASSED"
        ]

    def all_skipped(self):
        return [
            test_result
            for test_result in self.test_results
            if test_result.outcome == "SKIPPED"
        ]

    def all_xfails(self):
        return [
            test_result
            for test_result in self.test_results
            if test_result.outcome == "XFAIL"
        ]

    def all_xpasses(self):
        return [
            test_result
            for test_result in self.test_results
            if test_result.outcome == "XPASS"
        ]

    def all_errors(self):
        return [
            test_result
            for test_result in self.test_results
            if test_result.outcome == "ERROR"
        ]


@dataclass
class TuiSection:
    name: str = ""
    content: str = ""


@dataclass
class TuiSections:
    live_log_sessionstart: TuiSection = TuiSection(name="pre_test", content="")
    test_session_starts: TuiSection = TuiSection(name="test_session_starts", content="")
    errors: TuiSection = TuiSection(name="errors", content="")
    failures: TuiSection = TuiSection(name="failures", content="")
    passes: TuiSection = TuiSection(name="passes", content="")
    warnings_summary: TuiSection = TuiSection(name="warnings_summary", content="")
    short_test_summary: TuiSection = TuiSection(name="short_test_summary", content="")
    lastline: TuiSection = TuiSection(name="lastline", content="")


class Results:
    """
    This class holds all pertinent information for a given Pytest test run.
    """

    def __init__(self):
        """Top-level class attributes: TuiTestResults, TuiSections, and full console output w/ ANSI"""
        self.tui_test_info = self._unpickle_tui_test_info()
        self.tui_session_start_time = self.tui_test_info["sesssion_start_time"]
        self.tui_session_end_time = self.tui_test_info["sesssion_end_time"]
        self.tui_test_results = self.tui_test_info["tui_test_results"]
        self.tui_sections = self.tui_test_info["tui_sections"]
        self.terminal_output = self._get_terminal_output()

    def _unpickle_tui_test_info(self):
        """Unpack pickled results file"""
        try:
            with open(TUI_RESULTS_FILE, "rb") as rfile:
                return pickle.load(rfile)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Cannot find {TUI_RESULTS_FILE}. Have you run pytest with the '--tui' option yet?"
            ) from e

    def _get_terminal_output(self, file_path: Path = TERMINAL_OUTPUT_FILE) -> list:
        """Get full Pytest terminal output"""
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Cannot find {file_path}. Have you run pytest with the '--tui' option yet?"
            ) from e
            pass
