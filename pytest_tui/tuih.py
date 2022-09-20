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
from pytest_tui.utils import HTML_OUTPUT_FILE, TERMINAL_OUTPUT_FILE, Results

CSS_FILE = Path(__file__).parent / "resources" / "styles.css"
JS_FILE = Path(__file__).parent / "resources" / "scripts.js"

TAB_METADATA = ["About"]
TAB_METADATA_COLOR = {"About": "rgba(0, 0, 255, 0.33)"}
TABS_RESULTS = ["All Tests", "Failures", "Passes", "Skipped", "Xfails", "Xpasses"]
TABS_RESULTS_COLORS = {
    "All Tests": ("rgba(111, 104, 105, 0.34)", "rgba(128,128,0,0.5)"),
    "Failures": ("rgba(255, 10, 10, 0.75)", "rgba(255,0,0,0.5)"),
    "Passes": ("rgba(66, 228, 47, 1)", "rgba(0,0,0,0.5)"),
    "Skipped": ("rgba(111, 104, 105, 0.34)", "rgba(128,128,0,0.5)"),
    "Xfails": ("rgba(255, 176, 176, 0.90)", "rgba(0,0,0,0.5)"),
    "Xpasses": ("rgba(0, 255, 0, 0.43)", "rgba(0,0,0,0.5)"),
}
TABS_SECTIONS = [
    "summary_section",
    "failures_section",
    "passes_section",
    "warnings_section",
    "errors_section",
]
TABS_SECTIONS_COLORS = {
    "summary_section": "#daeaf6",
    "failures_section": "rgba(255, 10, 10, 0.50)",
    "passes_section": "rgba(66, 228, 47, 0.6)",
    "warnings_section": "#ffee93",
    "errors_section": "#ffc09f",
}
TAB_FULL_OUTPUT = ["Console Output"]
TAB_FULL_OUTPUT_COLOR = {"Console Output": "rgba(0, 0, 255, 0.33)"}


class TabContent:
    def __init__(self, results: Results):
        self.converter = Ansi2HTMLConverter()
        self.tabs = {tab: "" for tab in TABS_SECTIONS}
        self.results = results

    def add(self, tab, content):
        self.tabs[tab] = content

    def get_all_items(self):
        return self.tabs

    def fetch_raw_section(self):
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

        return self.get_all_items()

    def fetch_sections_html(self):
        return {
            key: self.converter.convert(value, full=False)
            for key, value in self.fetch_raw_section().items()
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

    def create_trailer(self) -> str:
        return """</script> </body> </html>"""

    def create_tabs(self) -> str:
        tabs_links = [
            f"""<button class="tablinks" style="background-color: {TAB_METADATA_COLOR[section]}" id="defaultOpen" onclick="openTab(event, '{section}')" >{section}</button>"""
            for section in TAB_METADATA
        ]

        tabs_links.extend(
            [
                f"""<button class="tablinks" style="background-color: {TABS_RESULTS_COLORS[section][0]}" onclick="openTab(event, '{section}')" >{section}</button>"""
                for section in TABS_RESULTS
            ]
        )

        tabs_links.extend(
            [
                """<div class="dropdown"> <button class="dropbtn" style="color: white; background-color: gray">Output Sections</button> <div id="myDropdown" class="dropdown-content">"""
            ]
        )

        tabs_links.extend(
            [
                f"""<button class="dropdown-item tablinks" style="background-color: {TABS_SECTIONS_COLORS[section]}" onclick="openTab(event, '{section}')" >{section}</button>"""
                for section in TABS_SECTIONS
            ]
        )

        tabs_links.extend(["""</div> </div>"""])

        tabs_links.extend(
            [
                f"""<button class="tablinks" style="background-color: {TAB_FULL_OUTPUT_COLOR[section]}" onclick="openTab(event, '{section}')" >{section}</button>"""
                for section in TAB_FULL_OUTPUT
            ]
        )

        tab_links_section = """<div class="tab">""" + "".join(tabs_links) + """</div>"""

        tab_links_section += """</div>"""

        tab_result_content = []
        for result in TABS_RESULTS:
            if result == "All Tests":
                tab_result_content.append(
                    f"""<div id="{result}" class="tabcontent"> {self.get_collapsible_results("tests")} </div>"""
                )
            else:
                tab_result_content.append(
                    f"""<div id="{result}" class="tabcontent"> {self.get_collapsible_results(result.lower())} </div>"""
                )

        tab_results = "".join(tab_result_content)

        tab_section_content = [
            f"""<div id="{section}" class="tabcontent"> <pre>{self.converter.convert(self.tab_content.tabs[section], full=False) or ""}</pre> </div>"""
            for section in TABS_SECTIONS
            if self.tab_content.tabs[section]
        ]
        tab_sections = "".join(tab_section_content)

        tab_metadata = f"""<div id="{TAB_METADATA[0]}" class="tabcontent"> <p>{self.get_metadata()}</p> </div>"""

        tab_fullout = f"""<div id="{TAB_FULL_OUTPUT[0]}" class="tabcontent"> <pre>{self.get_terminal_output()}</pre> </div>"""

        return (
            tab_links_section + tab_metadata + tab_results + tab_sections + tab_fullout
        )

    def get_collapsible_results(self, outcome) -> str:
        collapsible_results = ""
        results_by_outcome = eval(f"self.results.tui_test_results.all_{outcome}()")
        for result in results_by_outcome:
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
        md = [line for line in lines if line.startswith("metadata: {")][0]
        m = json.loads(md.replace("'", '"').lstrip("metadata: "))
        m.pop("JAVA_HOME")
        now = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        results_modification_time = (
            datetime.utcfromtimestamp(Path(TERMINAL_OUTPUT_FILE).stat().st_mtime)
            .replace(microsecond=0)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
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
            f"{self.create_testrun_results()}<hr>"
            + f"""<h5>Test results generated:</h5> <p>{results_modification_time}</p>"""
            + f"""<h5>This report generated:</h5> <p>{now}</p>"""
            + f"""<h5>pytest-tui version:</h5> <p>{__version__}</p><hr>"""
            + """<h5><b>Meta Data / Environment:</b></h5>"""
            + json2table.convert(
                m, build_direction="LEFT_TO_RIGHT", table_attributes=table_attributes
            )
        )

    def get_terminal_output(self) -> str:
        with open(TERMINAL_OUTPUT_FILE, "rb") as f:
            tout = str(f.read(), "utf-8")
        return self.converter.convert(tout, full=False)

    def get_js(self) -> str:
        with open(Path(JS_FILE), "r") as f:
            lines = f.readlines()
        return "".join(f"<script>{line}</script>" for line in lines if line.strip("\n"))


def main():
    results = Results()
    page = HtmlPage(results)
    page.remove_tabs_without_content()
    html_header = page.create_header()
    html_tabs = page.create_tabs()
    html_trailer = page.create_trailer()
    my_js = page.get_js()
    html_out = html_header + html_tabs + "\n" + my_js + html_trailer

    with open(HTML_OUTPUT_FILE, "w+") as f:
        f.write(html_out)

    webbrowser.open(f"file://{HTML_OUTPUT_FILE._str}")



    # Open in browser if autolaunch_html config is set
    # page.cli.read_config_file()
    # if page.cli.html_autolaunch:
    #     webbrowser.open(f"file://{HTML_OUTPUT_FILE._str}")


if __name__ == "__main__":
    main()
