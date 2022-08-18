import html
import json
import webbrowser

import json2table
from ansi2html import Ansi2HTMLConverter
from strip_ansi import strip_ansi

from pytest_tui import __version__
from pytest_tui.utils import Results

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
        return {
            key: self.converter.convert(value, full=False)
            for key, value in self.fetch_raw().items()
        }


class HtmlPage:
    def __init__(
        self,
    ):
        self.tab_content = TabContent().fetch_html()

    def create_header(self) -> str:
        return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>pytest-tui html report</title> <link rel="stylesheet" href="pytest_tui/styles.css"> </head> <body class="body_foreground body_background" style="font-size: normal;" >"""

    def create_trailer(self) -> str:
        return """</body> </html>"""

    def create_tabs(self) -> str:
        tabs_links = [
            f"""<button class="tablinks" onclick="openTab(event, '{section}')" >{section}</button>"""
            for section in TAB_METADATA + TABS_SECTIONS
        ]
        # tabs_links.append("""<button class="tablinks" onclick="openTab(event, 'Summary')" id="defaultOpen" >Summary</button>""")
        tab_links_section = """<div class="tab">""" + "".join(tabs_links) + """</div>"""
        tab_section_content = [
            f"""<div id="{section}" class="tabcontent"> <h3>{section}</h3> <pre><p>{self.tab_content[section]}</p></pre> </div>"""
            for section in TABS_SECTIONS
        ]
        tab_content_section = "".join(tab_section_content)
        tab_metadata_content = f"""<div id="{TAB_METADATA[0]}" class="tabcontent"> <h3>{TAB_METADATA[0]}</h3> <pre><p>{self.get_metadata()}</p></pre> </div>"""
        return tab_links_section + tab_content_section + tab_metadata_content

    def create_tab_script(self) -> str:
        return """<script> function openTab(evt, tabName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(tabName).style.display = "block"; evt.currentTarget.className += " active"; } </script>"""

    def create_tab_toggle_script(self) -> str:
        return """<script function toggle_tab(evt, tabName) { if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } } </script>"""

    def create_default_open(self) -> str:
        return """<script> document.getElementById("defaultOpen").click(); </script>"""

    def create_cdn(self) -> str:
        return """"""

    def get_metadata(self) -> str:
        lines = results.tui_sections.test_session_starts.content.split("\n")
        return lines[3]


def main():
    conv = Ansi2HTMLConverter()
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
