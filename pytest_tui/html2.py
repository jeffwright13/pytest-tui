import html
import json
from lib2to3.pytree import convert
import webbrowser

import json2table
from ansi2html import Ansi2HTMLConverter

from pytest_tui import __version__
from pytest_tui.utils import Results, TERMINAL_OUTPUT_FILE

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
TAB_METADATA = ["Metadata"]
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
        pass

    def create_header(self) -> str:
        return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>pytest-tui html report</title> <link rel="stylesheet" href="pytest_tui/styles.css"> </head> <body class="body_foreground body_background" style="font-size: normal;" >"""

    def create_trailer(self) -> str:
        return """</body> </html>"""

    def create_tabs(self) -> str:
        # Create tabs for sections, results, full-out, metadata
        tabs_links = [
            f"""<button class="tablinks" onclick="openTab(event, '{section}')" >{section}</button>"""
            for section in TAB_METADATA + TABS_SECTIONS + TAB_FULL_OUTPUT
        ]
        tab_links_section = """<div class="tab">""" + "".join(tabs_links) + """</div>"""
        tab_section_content = [
            f"""<div id="{section}" class="tabcontent"> <h3>{section}</h3> <pre><p>{self.tab_content[section]}</p></pre> </div>"""
            for section in TABS_SECTIONS
        ]
        tab_content_section = "".join(tab_section_content)
        tab_metadata_content = f"""<div id="{TAB_METADATA[0]}" class="tabcontent"> <h3>{TAB_METADATA[0]}</h3> <p>{self.get_metadata()}</p> </div>"""
        tab_fullout_content = f"""<div id="{TAB_FULL_OUTPUT[0]}" class="tabcontent"> <h3>{TAB_FULL_OUTPUT[0]}</h3> <pre><p>{self.get_terminal_output()}</p></pre> </div>"""
        return (
            tab_links_section
            + tab_content_section
            + tab_metadata_content
            + tab_fullout_content
        )

    def create_tab_script(self) -> str:
        return """<script> function openTab(evt, tabName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(tabName).style.display = "block"; evt.currentTarget.className += " active"; } </script>"""

    def create_tab_toggle_script(self) -> str:
        return """<script function toggle_tab(evt, tabName) { if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } } </script>"""

    def create_default_open(self) -> str:
        return """<script> document.getElementById("defaultOpen").click(); </script>"""

    def create_cdn(self) -> str:
        return """"""

    # def get_terminal_output(self) -> str:
    #     return results.tui_sections.lastline.content

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
            "font-family": "Helvetica, Arial, sans-serif",
            "border": "1",
            "style": "width:auto%; table-layout: auto;",
            "border-collapse": "collapse",
            "class": "data-table",
            "class": "sortable",
            "text-align": "left",
            "tr": "nth-child(even) {background-color: #f2f2f2;}",
        }
        return json2table.convert(m, table_attributes=table_attributes)

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
    html_scripts = html_tab_script + html_default_open
    html_out = html_header + html_tabs + html_scripts + html_trailer

    with open("html2.html", "w+") as f:
        f.write(html_out)


if __name__ == "__main__":
    main()
