import json
import webbrowser
from datetime import datetime, timezone

import json2table
from ansi2html import Ansi2HTMLConverter

from pytest_tui import __version__
from pytest_tui.utils import TERMINAL_OUTPUT_FILE, Results

TABS = [
    "Summary",
    "Failures",
    "Passes",
    "Skipped",
    "Xfails",
    "Xpasses",
    "Reruns",
    "Warnings",
    "Errors",
    "Full Output",
]
TABS_SECTIONS = [
    "summary_section",
    "warnings_section",
    "errors_section",
    "passes_section",
    "failures_section",
    "reruns_section",
]
TABS_RESULTS = ["Failures", "Passes", "Skipped", "Xfails", "Xpasses", "Reruns"]
TAB_METADATA = ["About"]
TAB_FULL_OUTPUT = ["Full Output"]

results = Results()


class TabContent:
    def __init__(self):
        self.converter = Ansi2HTMLConverter()
        self.tabs = {tab: "" for tab in TABS}

    def add(self, tab, content):
        self.tabs[tab] = content

    def get(self, tab):
        return self.tabs[tab]

    def get_all(self):
        return self.tabs

    def get_all_items(self):
        return self.tabs

    def fetch_raw(self):
        self.add(
            "summary_section",
            results.tui_sections.lastline.content
            + results.tui_sections.test_session_starts.content
            + results.tui_sections.short_test_summary.content,
        )
        self.add("warnings_section", results.tui_sections.warnings_summary.content)
        self.add("errors_section", results.tui_sections.errors.content)
        self.add("passes_section", results.tui_sections.passes.content)
        self.add("failures_section", results.tui_sections.failures.content)
        self.add("reruns_section", results.tui_sections.rerun_summary.content)
        return self.get_all_items()

    def fetch_html(self):
        reset = "\x1b[0m"
        return {
            key: self.converter.convert(value, full=False)
            for key, value in self.fetch_raw().items()
        }


class HtmlPage:
    def __init__(
        self,
    ):
        self.tab_content = TabContent().fetch_html()
        self.converter = Ansi2HTMLConverter()

    def create_header(self) -> str:
        return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>pytest-tui html report</title> <link rel="stylesheet" href="pytest_tui/styles.css"> </head> <body class="body_foreground body_background" style="font-family: 'Helvetica, Arial, sans-serif';   font-size: normal;" >"""

    def create_trailer(self) -> str:
        return """</body> </html>"""

    def create_tabs(self) -> str:
        # Create tabs for sections, results, full-out, metadata
        tabs_links = [
            f"""<button class="tablinks" onclick="openTab(event, '{section}')" >{section}</button>"""
            for section in TAB_METADATA + TABS_RESULTS + TABS_SECTIONS + TAB_FULL_OUTPUT
        ]
        tab_links_section = """<div class="tab">""" + "".join(tabs_links) + """</div>"""

        # Results tabs
        tests_by_outcome_and_time = results.tui_test_results.all_by_outcome_then_time()
        results_failures = [
            result for result in tests_by_outcome_and_time if result.outcome == "FAILED"
        ]

        tab_result_content = [
            f"""<div id="{result}" class="tabcontent"> <h3>{result}</h3> <pre><p>{self.get_collapsible_results(result.lower())}</p></pre> </div>"""
            for result in TABS_RESULTS
        ]
        tab_results = "".join(tab_result_content)

        def _results_area(self):
            section_or_result_button_start = (
                """<button type="button" class="collapsible">"""
            )
            section_or_result_button_end = """</button> <div class="content"> <p>"""
            section_or_result_end = """</p> </div>"""

        # Sections tabs
        tab_section_content = [
            f"""<div id="{section}" class="tabcontent"> <h3>{section}</h3> <pre><p>{self.tab_content[section]}</p></pre> </div>"""
            for section in TABS_SECTIONS
        ]
        tab_sections = "".join(tab_section_content)

        # Metadata tab
        tab_metadata = f"""<div id="{TAB_METADATA[0]}" class="tabcontent"> <p>{self.get_metadata()}</p> </div>"""
        tab_fullout = f"""<div id="{TAB_FULL_OUTPUT[0]}" class="tabcontent"> <h3>{TAB_FULL_OUTPUT[0]}</h3> <pre><p>{self.get_terminal_output()}</p></pre> </div>"""
        return (
            tab_links_section + tab_metadata + tab_results + tab_sections + tab_fullout
        )

    def get_collapsible_results(self, outcome) -> str:
        collapsible_results = ""
        results_by_outcome = eval(f"results.tui_test_results.all_{outcome}()")
        for result in results_by_outcome:
            content = self.converter.convert(
                result.caplog
                + result.capstderr
                + result.capstdout
                + result.longreprtext,
                full=False,
            )
            if not content:
                content = "No output"
            collapsible_results += f"""<button type="button" class="collapsible" style="border: none; outline: none; background: none;">{result.fqtn}</button> <div class="content"> <p>{content}</p> </div>"""
        return collapsible_results

    def create_tab_script(self) -> str:
        return """<script> function openTab(evt, tabName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(tabName).style.display = "block"; evt.currentTarget.className += " active"; } </script>"""

    def create_tab_toggle_script(self) -> str:
        return """<script function toggle_tab(evt, tabName) { if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } } </script>"""

    def create_collapsible_script(self) -> str:
        return """<script> var coll = document.getElementsByClassName("collapsible"); var i; for (i = 0; i < coll.length; i++) { coll[i].addEventListener("click", function() { this.classList.toggle("active"); var content = this.nextElementSibling; if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }); } </script>"""

    def create_default_open(self) -> str:
        return """<script> document.getElementById("defaultOpen").click(); </script>"""

    def create_cdn(self) -> str:
        return """"""

    def create_html(self) -> str:
        return self.create_header() + self.create_tabs() + self.create_trailer()

    def create_html_file(self, filename: str):
        with open(filename, "w") as f:
            f.write(self.create_html())

    def create_html_file_with_script(self, filename: str):
        with open(filename, "w") as f:
            f.write(self.create_html())
            f.write(self.create_tab_script())
            f.write(self.create_tab_toggle_script())
            f.write(self.create_default_open())
            f.write(self.create_cdn())

    def get_metadata(self) -> str:
        lines = results.tui_sections.test_session_starts.content.split("\n")
        md = [line for line in lines if line.startswith("metadata: {")][0]
        m = json.loads(md.replace("'", '"').lstrip("metadata: "))
        m.pop("JAVA_HOME")
        table_attributes = {
            "id": "metadata",
            "font-family ": "Helvetica, Arial, sans-serif",
            "border": "1",
            "style": "width:auto%; table-layout: auto;",
            "border-collapse": "collapse",
            "class": "data-table",
            "class": "sortable",
            "text-align": "left",
            "tr": "nth-child(even) {background-color: #f2f2f2;}",
        }
        return (
            f"""<h4> Report generated on {datetime.now(timezone.utc).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')} UTC by pytest-tui version {__version__}</h4><hr>"""
            + json2table.convert(m, table_attributes=table_attributes)
        )

    def get_terminal_output(self) -> str:
        converter = Ansi2HTMLConverter()
        with open(TERMINAL_OUTPUT_FILE, "r") as f:
            tout = f.read()
        return converter.convert(tout, full=False)


def main():
    page = HtmlPage()
    html_header = page.create_header()
    html_tabs = page.create_tabs()
    html_tab_script = page.create_tab_script()
    html_default_open = page.create_default_open()
    html_trailer = page.create_trailer()
    html_cdn = page.create_cdn()
    html_collapsible_result_script = page.create_collapsible_script()
    html_scripts = html_tab_script + html_default_open + html_collapsible_result_script
    html_out = html_header + html_tabs + html_scripts + html_trailer

    with open("html2.html", "w+") as f:
        f.write(html_out)


if __name__ == "__main__":
    main()
