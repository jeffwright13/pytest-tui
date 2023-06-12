import argparse

# import configparser
import json
import logging
import re
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Union

import json2table
from ansi2html import Ansi2HTMLConverter
from strip_ansi import strip_ansi

from pytest_tui import __version__
from pytest_tui.utils import (
    DEFAULT_HTML_FILE,
    PYTEST_TUI_FILES_DIR,
    TERMINAL_OUTPUT_FILE,
    Results,
    test_session_starts_results_grabber,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CSS_FILE = Path(__file__).parent / "resources" / "styles.css"
JS_FILE = Path(__file__).parent / "resources" / "scripts.js"

TAB_ABOUT = ["About"]
TAB_ABOUT_COLOR = {"About": "hsl(199, 100%, 50%)"}
TABS_RESULTS = [
    "All Tests",
    "Failures",
    "Passes",
    "Skipped",
    "Xfails",
    "Xpasses",
    "Reruns",
]
TABS_RESULTS_COLORS = {
    "All Tests": ("hsl(64, 11%, 68%)", "rgba(128,128,0,0.5)"),
    "Failures": ("hsl(348, 78%, 53%)", "rgba(255,0,0,0.5)"),
    "Passes": ("rgba(66, 228, 47, 1)", "rgba(0,0,0,0.5)"),
    "Skipped": ("hsl(172, 21%, 59%)", "rgba(128,128,0,0.5)"),
    "Xfails": ("rgba(255, 176, 176)", "rgba(0,0,0,0.5)"),
    "Xpasses": ("hsl(141, 45%, 48%)", "rgba(0,0,0,0.5)"),
    "Reruns": ("rgba(220,165.0,1)", "rgba(255,194,0,0.5)"),
}

TAB_FULL_OUTPUT = ["Full Output"]
TAB_FULL_OUTPUT_COLOR = {"Full Output": "hsl(195, 100%, 47%)"}

TAB_FOLDED_OUTPUT = ["Folded Output"]
TAB_FOLDED_OUTPUT_COLOR = {"Folded Output": "rgba(0, 225, 128, 1)"}
TABS_SECTIONS = [
    "summary_section",
    "failures_section",
    "passes_section",
    "warnings_section",
    "errors_section",
    "reruns_section",
]
TABS_SECTIONS_COLORS = {
    "summary_section": "#daeaf6",
    "failures_section": "rgba(255, 10, 10, 0.50)",
    "passes_section": "rgba(66, 228, 47, 0.6)",
    "warnings_section": "#ffee93",
    "errors_section": "#ffc09f",
    "reruns_section": "#f6e3da",
}

TAB_ACTIONS = ["Actions"]
TAB_ACTIONS_COLOR = {"Actions": "rgba(249, 123, 64, 0.95)"}
TABS_ACTIONS = {
    "fold_action": "toggleAllDetails",
    "hide_action": "toggleDetailsElements",
}
TABS_ACTIONS_COLORS = {
    "fold_action": "#ffee93",
    "hide_action": "#ffc09f",
}


class TabContent:
    def __init__(self, results: Results):
        self.converter = Ansi2HTMLConverter()
        self.tabs = {tab: "" for tab in TABS_SECTIONS}
        self.results = results

    def add(self, tab, content):
        self.tabs[tab] = content

    def get_all_items(self):
        return self.tabs

    def fetch_raw_sections(self):
        summary_section = (
            "\n"
            + self.results.tui_sections.lastline.content
            + "\n"
            + self.results.tui_sections.test_session_starts.content
            + self.results.tui_sections.short_test_summary.content
        )
        self.add("summary_section", summary_section)
        self.add("warnings_section", self.results.tui_sections.warnings_summary.content)
        self.add("errors_section", self.results.tui_sections.errors.content)
        self.add("passes_section", self.results.tui_sections.passes.content)
        self.add("failures_section", self.results.tui_sections.failures.content)
        self.add("reruns_section", self.results.tui_sections.rerun_test_summary.content)

        return self.get_all_items()

    def fetch_sections_html(self):
        return {
            key: self.converter.convert(value, full=False)
            for key, value in self.fetch_raw_sections().items()
        }


class HtmlPage:
    def __init__(self, results: Results):
        self.results = results
        self.tab_content = TabContent(results)
        self.fetched_sections_html = self.tab_content.fetch_sections_html()
        self.converter = Ansi2HTMLConverter()

    def remove_tabs_without_content(self):
        # Remove tabs for sections that do not contain any data.
        # This way, the HTML file will not show blank section tabs.
        for tab in TABS_SECTIONS.copy():
            if not self.fetched_sections_html[tab]:
                TABS_SECTIONS.remove(tab)

        # Remove tabs for outcomes that have no test results.
        # This way, the HTML file will not show blank results tabs.
        if not self.results.tui_test_results.all_tests():
            TABS_RESULTS.remove("All Tests")
        if not self.results.tui_test_results.all_failures():
            TABS_RESULTS.remove("Failures")
        if not self.results.tui_test_results.all_passes():
            TABS_RESULTS.remove("Passes")
        if not self.results.tui_test_results.all_skipped():
            TABS_RESULTS.remove("Skipped")
        if not self.results.tui_test_results.all_xpasses():
            TABS_RESULTS.remove("Xpasses")
        if not self.results.tui_test_results.all_xfails():
            TABS_RESULTS.remove("Xfails")
        if not self.results.tui_test_results.all_reruns():
            TABS_RESULTS.remove("Reruns")

    def create_header(self) -> str:
        my_css = Path(CSS_FILE).read_text().replace("\n", "")
        return f"""<!DOCTYPE html> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8, width=device-width, initial-scale=1.0"> <title>Test Run Results</title> <style> {my_css} </style> </head> <body class="body_foreground body_background" style="font-family: 'Helvetica, Arial, sans-serif';" > <div class="sticky">"""

    def create_testrun_results(self) -> str:
        return (
            """<hr><h5>Final Results:</h5><pre><b>"""
            + self.converter.convert(
                self.results.tui_sections.lastline.content.replace("=", ""), full=False
            )
            + """</b></pre>"""
        )

    def create_final_test_summary(self) -> str:
        return (
            """<button class="accordion-open">Final Test Summary  (click to expand)</button><div class="panel-open"><p><pre>"""
            + self.converter.convert(
                self.results.tui_sections.short_test_summary.content, full=False
            )
            + "\n"
            + self.converter.convert(
                self.results.tui_sections.lastline.content, full=False
            )
            + """</pre></p></div>"""
        )

    def create_live_test_session_summary(self) -> str:
        search = re.search(
            test_session_starts_results_grabber,
            self.results.tui_sections.test_session_starts.content.encode(
                "unicode_escape"
            ).decode(),
        )
        ripped = search.groups()[0].encode().decode("unicode-escape") if search else ""
        return (
            """<button class="accordion-open">Live Test Session Summary  (click to expand)</button><div class="panel-open"><p><pre>"""
            + self.converter.convert(
                self.results.tui_sections.lastline.content, full=False
            )
            + self.converter.convert(ripped, full=False)
            + self.converter.convert(
                self.results.tui_sections.lastline.content, full=False
            )
            + """</pre></p></div>"""
        )

    def create_test_execution_info(self) -> str:
        now = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        table_attributes = {
            "id": "test_execution_info",
            "font-family": "Helvetica, Arial, sans-serif",
            "font-size": "12px",
            "border": "ridge",
            "style": "width:auto%; table-layout: auto;",
            "border-collapse": "collapse",
            "text-align": "left",
            "tr": "nth-child(even) {background-color: #f2f2f2;}",
        }
        d = {
            "Test run started": f"{self.results.tui_session_start_time} UTC",
            "Test run completed": f"{self.results.tui_session_end_time} UTC",
            "Test run duration": f"{self.results.tui_session_duration}",
            "This report generated": f"{now} UTC",
            "pytest-tui version": f"{__version__}",
        }
        dj = json2table.convert(
            d, build_direction="LEFT_TO_RIGHT", table_attributes=table_attributes
        )
        return (
            """<button class="accordion-closed">Test Execution Info (click to expand)</button><div class="panel-closed"><p><pre>"""
            + dj
            + """</pre></p></div>"""
        )

    def create_environment_info(self, m, table_attributes) -> str:
        return (
            """<button class="accordion-closed">Environment (click to expand)</button><div class="panel-closed"><p><pre>"""
            + json2table.convert(
                m, build_direction="LEFT_TO_RIGHT", table_attributes=table_attributes
            )
            + """</pre></p></div>"""
        )

    def get_js(self) -> str:
        """
        Gets JS from scripts.js and wraps them in <script> tags.
        Note that in the scripts.js file, all scripts MUST e one-liners.
        """
        with open(Path(JS_FILE), "r") as f:
            lines = f.readlines()
        return "".join(f"<script>{line}</script>" for line in lines if line.strip("\n"))

    def create_trailer(self) -> str:
        return f"""{self.get_js()} </script> </body> </html>"""

    def create_tabs(self) -> str:
        tabs_links = [
            f"""<div class="sticky"> <span><button class="tablinks" style="background-color: {TAB_ABOUT_COLOR[section]}" id="defaultOpen" onclick="openTab(event, '{section}')" >{section}</button></span>"""
            for section in TAB_ABOUT
        ]

        tabs_links.extend(
            [
                f"""<span><button class="tablinks" style="background-color: {TABS_RESULTS_COLORS[section][0]}" onclick="openTab(event, '{section}')" >{section}</button></span>"""
                for section in TABS_RESULTS
            ]
        )

        # Dropdown for output sections
        tabs_links.extend(
            [
                """<span class="dropdown"> <button class="dropbtn" style="color: #dddddd; background-color: gray">Output Sections</button> <span class="dropdown-content">"""
            ]
        )
        tabs_links.extend(
            [
                f"""<span><button class="dropdown-item tablinks" style="background-color: {TABS_SECTIONS_COLORS[section]}" onclick="openTab(event, '{section}')" >{section}</button></span>"""
                for section in TABS_SECTIONS
            ]
        )
        tabs_links.extend(["""</span> </span>"""])

        # Full Output tab
        tabs_links.extend(
            [
                f"""<span><button class="tablinks" style="background-color: {TAB_FULL_OUTPUT_COLOR[section]}" onclick="openTab(event, '{section}')" >{section}</button></span>"""
                for section in TAB_FULL_OUTPUT
            ]
        )

        # This variable determines if the "Folded Output" tab and "Fold Actions" tabs are displayed or not
        fold_visibility = "" if self.results.tui_regexfile else "display: none;"
        if self.results.tui_regexfile:
            tabs_links.extend(
                [
                    """<span class="dropdown"> <button class="dropbtn" style="color: brown; background-color: #d9ead3">Fold Actions</button> <span class="dropdown-content">"""
                ]
            )
            tabs_links.extend(
                [
                    """<span><button class="dropdown-item tablinks" style="background-color: #a8b3dc" onclick="toggleAllDetails()">Fold / Unfold</button> </span>"""
                ]
            )
            # tabs_links.extend(
            #     [
            #         """<span><button class="dropdown-item tablinks btn-rt" style="background-color: #b3dca8" id="toggle-details" onclick="toggleDetailsElements()">Hide / Show Fold Markers</button></span>"""
            #     ]
            # )
            tabs_links.extend(
                [
                    """<span><button class="dropdown-item tablinks btn-rt" style="background-color: #b3dca8" id="toggle-summary" onclick="toggleSummaryElements()">Hide / Show Fold Markers</button></span>"""
                ]
            )
            tabs_links.extend(["""</span> </span>"""])

        # The actual folded output content, tab "Folded Output" is just a container for this content
        tabs_links.extend(
            [
                f"""<span><button class="tablinks" style="{fold_visibility} background-color: {TAB_FOLDED_OUTPUT_COLOR[section]}" onclick="openTab(event, '{section}')" >{section}</button></span> </div>"""
                for section in TAB_FOLDED_OUTPUT
            ]
        )

        # Stitch all the tabs together to be displayed at top of page
        tab_links_section = (
            """<span class="tab">""" + "".join(tabs_links) + """</span>"""
        )

        # Build up content for each tab that shows a results category (Pass, Fail, etc.)
        # Each results tab is populated with individual result content, each of which is collapsible
        tab_result_content = []
        for tab in TABS_RESULTS:
            if tab == "All Tests":
                tab_result_content.append(
                    f"""<div id="{tab}" class="tabcontent"> {self.get_collapsible_results("tests")} </div>"""
                )
            elif tab == "Reruns":
                tab_result_content.append(
                    f"""<div id="{tab}" class="tabcontent"> {self.get_collapsible_results("reruns")} </div>"""
                )
            else:
                tab_result_content.append(
                    f"""<div id="{tab}" class="tabcontent"> {self.get_collapsible_results(tab.lower())} </div>"""
                )

        # Stitch all the results together to be displayed withint their individual category tabs
        tab_results = "".join(tab_result_content)

        # Construct a single tab which drops down and displays individual Pytest output sections (e.g. "Summary", "Errors", etc.)
        # This content comes ANSI-encoded, so it needs to be converted to HTML for proper display
        tab_section_content = [
            f"""<div id="{section}" class="tabcontent"> <pre>{self.converter.convert(self.tab_content.tabs[section], full=False) or ""}</pre> </div>"""
            for section in TABS_SECTIONS
            if self.tab_content.tabs[section]
        ]
        tab_sections = "".join(tab_section_content)

        # The "About" tab (metadata, etc for this test run)
        tab_about = f"""<div id="{TAB_ABOUT[0]}" class="tabcontent"> <p>{self.get_metadata()}</p> </div>"""

        # The "Full Output" tab (all output from the test run), as it occured chronologically on the console
        tab_full_output = f"""<div id="{TAB_FULL_OUTPUT[0]}" class="tabcontent"> <pre>{self.get_terminal_output()}</pre> </div>"""

        # Folded Output tab; always generated but only displayed if self.results.tui_regexfile is True
        # (i.e. if the user provided a regex file)
        tab_folded_output = f"""<span id="{TAB_FOLDED_OUTPUT[0]}" class="tabcontent"> <pre>{self.fold_terminal_output_by_regex()}</pre> </span>"""

        return (
            tab_links_section
            + tab_about
            + tab_results
            + tab_full_output
            + tab_sections
            + tab_folded_output
        )

    def get_collapsible_results(self, outcome) -> str:
        collapsible_results = ""
        if outcome == "reruns":
            results = []
            for group in self.results.tui_rerun_test_groups:
                for result in group.full_test_list:
                    results.append(result)
        else:
            results = eval(f"self.results.tui_test_results.all_{outcome}()")

        for result in results:
            content_ansi = (
                result.caplog
                + result.capstderr
                + result.capstdout
                + result.longreprtext
            )
            if self.results.tui_regexfile:
                content_html = self.fold_regex_lines(content_ansi.splitlines())
            else:
                content_html = self.converter.convert(content_ansi, full=False)
            if not content_html:
                content_html = "No output was produced for this test"

            collapsible_results += f"""<button type="button" class="collapsible" style="border: none; outline: none;">{re.sub(r".[0-9]*$", "", str(result.start_time))} | {result.outcome} | {result.fqtn}</button> <div class="content"> <pre>{content_html}</pre> </div>"""
        return collapsible_results

    def get_metadata(self) -> str:
        lines = self.results.tui_sections.test_session_starts.content.split("\n")
        try:
            md = [line for line in lines if line.startswith("metadata: {")][0]
        except IndexError:
            return ""
        m = json.loads(md.replace("'", '"').lstrip("metadata: "))
        m.pop("JAVA_HOME") if "JAVA_HOME" in m else None
        table_attributes = {
            "id": "metadata",
            "font-family": "Helvetica, Arial, sans-serif",
            "font-size": "12px",
            "border": "ridge",
            "style": "width:auto%; table-layout: auto;",
            "border-collapse": "collapse",
            "text-align": "left",
            "tr": "nth-child(even) {background-color: #f2f2f2;}",
        }

        # tab_color_button =  """<rainbow-button onclick="removeColor()">Remove color</rainbow-button>"""
        # tab_color_button =  """<button class=button-43 onclick="removeColor(); this.style.display = 'none'">Remove Color</button>"""
        tab_color_button = """<button class="button-43" onclick="removeOrRestoreColor()">Remove / Restore Colors</button>"""
        tab_invert_button = """<button class=button-43 onclick="invertColors()">Invert Colors</button>"""
        tab_toggle_background_button = """<button class="button-43" onclick="togglePreBackground()">Toggle Background</button>"""

        return (
            "<hr>"
            + f"{self.create_final_test_summary()}<hr>"
            + f"{self.create_live_test_session_summary()}<hr>"
            + f"{self.create_test_execution_info()}<hr>"
            + f"{self.create_environment_info(m, table_attributes)}<hr>"
            + tab_color_button
            + "<hr>"
            + tab_invert_button
            + "<hr>"
            + tab_toggle_background_button
        )

    def get_terminal_output(self) -> str:
        with open(TERMINAL_OUTPUT_FILE, "rb") as f:
            tout = str(f.read(), "utf-8")
        return self.converter.convert(tout, full=False)

    def get_terminal_output_ansi(self) -> str:
        with open(TERMINAL_OUTPUT_FILE, "rb") as f:
            tout = str(f.read(), "utf-8")
        return tout

    def get_regex(self, tui_regexfile: Path) -> List[str]:
        """Read regex file and return list of regexes"""
        try:
            with open(tui_regexfile, "r") as file:
                # lines = [ast.literal_eval(line) for line in file.readlines() if line]
                lines = [eval(line) for line in file.readlines() if line]
                return [line.rstrip() for line in lines if line]
        except FileNotFoundError as e:
            logger.error(
                f"Regex file not found: {tui_regexfile}. Proceeding with folding"
                " feature disabled."
            )
            return []

    def fold_regex_lines(self, lines: List[str]) -> str:
        """
        Refactored code
        Search each line of console output and look for a regex match,
        using the regex patterns defined in file <tui-regexfile>.
        If a line contains a match for the regex patterrn, the line
        will be folded. Consecutive lines that match regex are grouped
        together within the same fold.
        """
        converter = Ansi2HTMLConverter()
        html_str = ""
        fold_started = False
        regexes = self.get_regex(self.results.tui_regexfile)

        if len(regexes) == 1:
            # If there is only one regex pattern, use it to fold any line that matches
            regex = regexes[0]
            for line in lines:
                line_stripped = strip_ansi(line)
                line_converted = converter.convert(line, full=False)
                match = re.search(regex, line_stripped)

                if match:
                    if not fold_started:
                        fold_started = True
                        html_str += (
                            "<details><summary style='nobr'>Folded RegEx:"
                            f" '{regex}'</summary>"
                        )
                    html_str += line_converted + "\n"
                elif fold_started:
                    fold_started = False
                    html_str += "</details>"
                    html_str += line_converted + "\n"
                else:
                    html_str += line_converted + "\n"

        if len(regexes) >= 2:
            # With 2 regexes, the first is the 'starter' regex and the second is the 'ender' regex
            regex_starter = regexes[0]
            regex_ender = regexes[1]
            for line in lines:
                line_stripped = strip_ansi(line)
                line_converted = converter.convert(line, full=False)
                match_starter = re.search(regex_starter, line_stripped)
                match_ender = re.search(regex_ender, line_stripped)

                if match_starter:
                    if not fold_started:
                        fold_started = True
                        html_str += (
                            "<details><summary style='nobr'>Folded RegEx:"
                            f" '{regex_starter}'</summary>"
                        )
                elif match_ender:
                    fold_started = False
                    html_str += "</details>"
                elif fold_started:
                    html_str += line_converted + "\n"
                else:
                    html_str += line_converted + "\n"

        return html_str

    def fold_terminal_output_by_regex(self) -> Union[str, None]:
        terminal_output_ansi = self.get_terminal_output_ansi()
        lines = terminal_output_ansi.splitlines()
        return self.fold_regex_lines(lines) if self.results.tui_regexfile else None

    def create_output_file(self, html_outfile: Path, html_out: str) -> None:
        assert isinstance(html_outfile, Path), "html_outfile must be a Path object"
        html_outfile.parent.mkdir(parents=True, exist_ok=True)
        with html_outfile.open("w") as f:
            f.write(html_out)
        logger.info(f"HTML report generated: {html_outfile}")


def main():
    results = Results()
    page = HtmlPage(results)
    page.remove_tabs_without_content()
    html_header = page.create_header()
    html_tabs = page.create_tabs()
    html_trailer = page.create_trailer()
    html_out = html_header + html_tabs + html_trailer

    html_outfile = Path(results.tui_test_info.get("tui_htmlfile", DEFAULT_HTML_FILE))
    page.create_output_file(html_outfile, html_out)


if __name__ == "__main__":
    main()
