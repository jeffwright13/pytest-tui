# import configparser
import json
import re
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

import json2table
from ansi2html import Ansi2HTMLConverter

from pytest_tui import __version__

# from pytest_tui.__main__ import Cli
# from pytest_tui.utils import CONFIGFILE, HTML_OUTPUT_FILE, TERMINAL_OUTPUT_FILE, Results
from pytest_tui.utils import (
    HTML_OUTPUT_FILE,
    LOG_LEVEL_MAP,
    PYTEST_TUI_FILES_DIR,
    TERMINAL_OUTPUT_FILE,
    TUI_FOLD_CONTENT_BEGIN,
    TUI_FOLD_CONTENT_END,
    TUI_FOLD_TITLE_BEGIN,
    TUI_FOLD_TITLE_END,
    Results,
    test_session_starts_results_grabber,
)

CSS_FILE = Path(__file__).parent / "resources" / "styles.css"
JS_FILE = Path(__file__).parent / "resources" / "scripts.js"

TAB_ABOUT = ["About"]
TAB_ABOUT_COLOR = {"About": "rgba(0, 0, 255, 0.33)"}
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
    "All Tests": ("rgba(111, 104, 105, 0.34)", "rgba(128,128,0,0.5)"),
    "Failures": ("rgba(255, 10, 10, 0.75)", "rgba(255,0,0,0.5)"),
    "Passes": ("rgba(66, 228, 47, 1)", "rgba(0,0,0,0.5)"),
    "Skipped": ("rgba(111, 104, 105, 0.34)", "rgba(128,128,0,0.5)"),
    "Xfails": ("rgba(255, 176, 176, 0.90)", "rgba(0,0,0,0.5)"),
    "Xpasses": ("rgba(0, 255, 0, 0.43)", "rgba(0,0,0,0.5)"),
    "Reruns": ("rgba(220,165.0,1)", "rgba(255,194,0,0.5)"),
}

TAB_FULL_OUTPUT = ["Full Output"]
TAB_FULL_OUTPUT_COLOR = {"Full Output": "rgba(0, 0, 255, 0.33)"}

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
        # Read existing config from file, or apply default if not exist
        # self.config_parser = configparser.ConfigParser()
        # self.cli = Cli()
        # self.cli.read_config_file()

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
        # my_css = Path(CSS_FILE).read_text().replace("\n", "")
        my_css = Path(CSS_FILE).read_text()
        return f"""<!DOCTYPE html> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8, width=device-width, initial-scale=1.0"> <title>Test Run Results</title> <style> {my_css} </style> </head> <body class="body_foreground body_background" style="font-family: 'Helvetica, Arial, sans-serif';" >"""

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
            """<button class="accordion">Final Test Summary  (click to expand)</button><div class="panel-closed"><p><pre>"""
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
            """<button class="accordion">Live Test Session Summary  (click to expand)</button><div class="panel-closed"><p><pre>"""
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
            """<button class="accordion">Test Execution Info</button><div class="panel-open"><p><pre>"""
            + dj
            + """</pre></p></div>"""
        )

    def create_environment_info(self, m, table_attributes) -> str:
        return (
            """<button class="accordion">Environment</button><div class="panel-open"><p><pre>"""
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
        # return (
        #     "".join(f"<script>{line}</script>" for line in lines if line.strip("\n"))
        # ).splitlines()

    def create_trailer(self) -> str:
        return f"""{self.get_js()} </script> </body> </html>"""

    def create_tabs(self) -> str:
        tabs_links = [
            f"""<span><button class="tablinks" style="background-color: {TAB_ABOUT_COLOR[section]}" id="defaultOpen" onclick="openTab(event, '{section}')" >{section}</button></span>"""
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

        # Dropdown for fold-section actions
        if self.results.tui_fold_level:
            tabs_links.extend(
                [
                    """<span class="dropdown"> <button class="dropbtn" style="color: brown; background-color: #d9ead3">Fold Actions</button> <span class="dropdown-content">"""
                ]
            )
            # tabs_links.extend(
            #     [
            #         f"""<span><button class="dropdown-item tablinks" style="background-color: {TABS_ACTIONS_COLORS[action]}" onclick="openAction(event, '{action}')" >{action}</button></span>"""
            #         for action in TABS_ACTIONS
            #     ]
            # )

            tabs_links.extend(
                [
                    """<span class="sticky"><button class="dropdown-item tablinks" style="background-color: #C7DBDF" onclick="toggleAllDetails()">Fold/Unfold Logs</button> </span>"""
                ]
            )
            tabs_links.extend(
                [
                    """<span class="sticky"><button class="dropdown-item tablinks btn-rt" style="background-color: #C7DBDF" id="toggle-details" onclick="toggleDetailsElements()">Show/Hide Fold Markers</button></span>"""
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

        if self.results.tui_fold_level:
            tabs_links.extend(
                [
                    f"""<span><button class="tablinks" style="background-color: {TAB_FOLDED_OUTPUT_COLOR[section]}" onclick="openTab(event, '{section}')" >{section}</button></span>"""
                    for section in TAB_FOLDED_OUTPUT
                ]
            )

        # tab_links_section += """</div>"""
        # tabs_links.extend(
        #     [
        #         f"""<button class="dropdown-item tablinks" style="background-color: {TAB_ACTIONS_COLOR[action]}" onclick="toggleDetails()">Actions</button>"""
        #         for action in TAB_ACTIONS
        #     ]
        # )
        tab_links_section = (
            """<span class="tab">""" + "".join(tabs_links) + """</span>"""
        )

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

        tab_results = "".join(tab_result_content)

        tab_section_content = [
            f"""<div id="{section}" class="tabcontent"> <pre>{self.converter.convert(self.tab_content.tabs[section], full=False) or ""}</pre> </div>"""
            for section in TABS_SECTIONS
            if self.tab_content.tabs[section]
        ]
        tab_sections = "".join(tab_section_content)

        tab_about = f"""<div id="{TAB_ABOUT[0]}" class="tabcontent"> <p>{self.get_metadata()}</p> </div>"""

        tab_full_output = f"""<div id="{TAB_FULL_OUTPUT[0]}" class="tabcontent"> <pre>{self.get_terminal_output()}</pre> </div>"""

        if self.results.tui_fold_level:
            tab_folded_output = f"""<span id="{TAB_FOLDED_OUTPUT[0]}" class="tabcontent"> <pre>{self.fold_terminal_output(self.results.tui_fold_level)}</pre> </span>"""
            # tab_action_hide_unhide_elements = """<span class="sticky">  <button class="dropdown-item tablinks btn-rt" style="background-color: #C7DBDF" id="toggle-details" onclick="toggleDetailsElements()">Show Folds</button>"""
            # tab_actions2 = """<button class="dropdown-item tablinks btn-rt" style="background-color: #B0D7DF" onclick="toggleDetails()">Fold/Unfold</button>"""
            # tab_actions3 = """<button style="background-color: #C7DBDF" onclick="openAllDetails()">Open all details</button>"""
            # tab_actions4 = """<button style="background-color: #B0D7DF"onclick="closeAllDetails()">Close all details</button>"""
            # tab_action_fold_unfold_details = """<button style="background-color: #C7DBDF" onclick="toggleAllDetails()">Toggle all details</button> </span>"""
            # tab_folded = tab_folded_output + tab_action_hide_unhide_elements + tab_action_fold_unfold_details
        else:
            tab_folded_output = ""

        everything = (
            tab_links_section
            + tab_about
            + tab_results
            + tab_sections
            + tab_full_output
            + tab_folded_output
        )
        return everything

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
            content = self.converter.convert(
                result.caplog
                + result.capstderr
                + result.capstdout
                + result.longreprtext,
                full=False,
            )
            if not content:
                content = "No output was produced for this test"
            collapsible_results += f"""<button type="button" class="collapsible" style="border: none; outline: none;">{re.sub(r".[0-9]*$", "", str(result.start_time))} | {result.outcome} | {result.fqtn}</button> <div class="content"> <pre>{content}</pre> </div>"""
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

        return (
            "<hr>"
            + f"{self.create_final_test_summary()}<hr>"
            + f"{self.create_live_test_session_summary()}<hr>"
            + f"{self.create_test_execution_info()}<hr>"
            + f"{self.create_environment_info(m, table_attributes)}"
        )

    def get_terminal_output(self) -> str:
        with open(TERMINAL_OUTPUT_FILE, "rb") as f:
            tout = str(f.read(), "utf-8")
        return self.converter.convert(tout, full=False)

    def get_terminal_output_ansi(self) -> str:
        with open(TERMINAL_OUTPUT_FILE, "rb") as f:
            tout = str(f.read(), "utf-8")
        return tout

    def get_line_level(self, line: str) -> str:
        """Is this line a log entry (DEBUG, INFO, WARNING, ERROR, CRITICAL)?"""
        for level, value in LOG_LEVEL_MAP.items():
            if level in line:
                return value

    def fold_log_lines(self, lines: list, level: str) -> str:
        """
        Search each line of console output and look for a log level indicator (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        If a line contains a log level indicator, check if log level is <= the level passed to the function.
        If the log level is <= the level passed to the function, then the line is folded.
        If the log level is > than the level passed to the function, then the line is not folded.
        """
        # sourcery skip: hoist-similar-statement-from-if, hoist-statement-from-if, merge-else-if-into-elif, merge-list-appends-into-extend
        html_lines = []
        html_str = ""
        fold_started = False
        for l in lines:
            line = self.converter.convert(l, full=False)
            this_line_log_level = self.get_line_level(l)
            if this_line_log_level:
                if this_line_log_level <= LOG_LEVEL_MAP[level]:
                    if not fold_started:
                        html_str += (
                            f"<details><summary style='nobr'>Folded {level}</summary>"
                        )
                        fold_started = True
                else:
                    if fold_started:
                        html_str += "</details>"
                        fold_started = False
                html_str += line + "\n"
            else:
                if fold_started:
                    html_str += "</details>"
                    fold_started = False
                    html_str += line + "\n"
                else:
                    html_str += line + "\n"
        return html_str

    def fold_terminal_output(self, level: str) -> str:
        terminal_output_ansi = self.get_terminal_output_ansi()
        lines = terminal_output_ansi.splitlines()
        return self.fold_log_lines(lines, level)

    # def fold_tracebacks(self, lines):
    #     html_lines = []
    #     folding = False
    #     for line in lines:
    #         if '_ test_' in line:
    #             if not folding:
    #                 html_lines.append("<details><summary>Folded DEBUG or INFO</summary>")
    #                 folding = True
    #         elif 'Captured log' in line and '-' in line:
    #             if folding:
    #                 html_lines.append('</details>')
    #                 folding = False
    #         html_lines.append(self.converter.convert(line, full=False))
    #     if folding:
    #         html_lines.append('</details>')
    #     return '\n'.join(html_lines)

    # def fold_terminal_output(self) -> str:
    #     terminal_output_ansi = self.get_terminal_output_ansi()
    #     lines = terminal_output_ansi.splitlines()
    #     return self.fold_tracebacks(lines)


def main():
    results = Results()
    page = HtmlPage(results)
    page.remove_tabs_without_content()
    html_header = page.create_header()
    html_tabs = page.create_tabs()
    # html_action_button = """<button class="dropdown-item tablinks btn-rt" style="background-color: rgba(249, 123, 64, 0.95)" onclick="toggleDetails()">Actions</button>"""
    html_trailer = page.create_trailer()
    html_out = html_header + html_tabs + html_trailer

    global HTML_OUTPUT_FILE
    if (
        "tui_htmlfile" in results.tui_test_info
        and results.tui_test_info["tui_htmlfile"].name
    ):
        HTML_OUTPUT_FILE = Path(
            PYTEST_TUI_FILES_DIR / results.tui_test_info["tui_htmlfile"]
        )
    with open(HTML_OUTPUT_FILE, "w+") as f:
        f.write(html_out)
    webbrowser.open(f"file://{HTML_OUTPUT_FILE._str}")

    # Open in browser if autolaunch_html config is set
    # page.cli.read_config_file()
    # if page.cli.html_autolaunch:
    #     webbrowser.open(f"file://{HTML_OUTPUT_FILE._str}")


if __name__ == "__main__":
    main()
