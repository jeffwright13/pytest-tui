import configparser
import json
import re
import webbrowser
from datetime import datetime, timezone

import json2table
from ansi2html import Ansi2HTMLConverter
from prettytable import PrettyTable
from strip_ansi import strip_ansi

from pytest_tui import __version__
from pytest_tui.__main__ import Cli
from pytest_tui.utils import CONFIGFILE, HTML_OUTPUT_FILE, Results


class HtmlPage:
    def __init__(
        self,
    ):
        # Read existing config from file, or apply default if not existing
        self.config_parser = configparser.ConfigParser()
        try:
            self.config_parser.read(CONFIGFILE)
        except Exception:
            Cli().apply_default_config()
            self.config_parser.read(CONFIGFILE)

        self.results = Results()
        self.sections = {
            "test session starts": self.results.tui_sections.test_session_starts.content,
            "short test summary info": self.results.tui_sections.lastline.content
            + self.results.tui_sections.short_test_summary.content,
            "warnings summary": self.results.tui_sections.warnings_summary.content,
            "errors": self.results.tui_sections.errors.content,
            "full output": self.results.terminal_output,
        }
        self.summary = self.results.tui_sections.lastline.content.replace("=", "")
        self.environment = []

    def read_environment(self) -> None:
        e = strip_ansi(self.results.tui_sections.test_session_starts.content).split(
            "\n"
        )[1:]
        for line in e:
            self.environment.append(line)
            if "collecting ... " in line:
                return

    def create_meta_table(self) -> None:
        """Create table of metadata ('environment' as shown in pytest-html)"""
        self.read_environment()
        metadata = json.loads(
            [line for line in self.environment if "metadata:" in line][0]
            .lstrip("metadata: ")
            .replace("'", '"')
        )
        metadata.pop("JAVA_HOME")
        self.metadata_table = json2table.convert(
            metadata,
            build_direction="LEFT_TO_RIGHT",
            table_attributes={
                "id": "metadata",
                "border": "1",
                "text-align": "left",
                "style": "width:100%",
                "border-collapse": "collapse",
            },
        )

    def clean(self, text: str) -> str:
        return re.sub("\\n+", "\\n", text)

    def create_results_table(self) -> None:

        """Create table of results"""
        conv = Ansi2HTMLConverter()
        x = PrettyTable()
        for test_result in self.results.tui_test_results.to_list():
            x.field_names = ["Test Name", "Outcome", "Start Time", "Duration"]
            x.add_row(
                [
                    test_result.fqtn,
                    test_result.outcome,
                    test_result.start_time,
                    test_result.duration,
                ]
            )
            x.add_row(
                [
                    test_result.caplog
                    + test_result.capstderr
                    + test_result.capstdout
                    + test_result.longreprtext,
                    "",
                    "",
                    "",
                ]
            )

        x.format = True

        attributes = {
            "id": "results",
            "border": "1",
            "style": "width:100%",
            "border-collapse": "collapse",
            "class": "data-table",
            "class": "sortable",
            "text-align": "left",
        }

        results_table = x.get_html_string(attributes=attributes)
        self.results_table = results_table.replace("<tr", '<tr class="item"')
        self.results_table = results_table.replace(
            "text-align: center", "text-align: left"
        )
        print("")


def main():  # sourcery skip: low-code-quality, use-fstring-for-concatenation
    conv = Ansi2HTMLConverter()
    page = HtmlPage()
    page.create_meta_table()

    scripty = """<script src= "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"> </script> <script src= "https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/js/bootstrap.min.js"> </script> <link rel="stylesheet" href= "https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/css/bootstrap.min.css"> <link rel="stylesheet" type="text/css" href= "https://use.fontawesome.com/releases/v5.6.3/css/all.css"> <script type="text/javascript"> function showHideRow(row) { $("#" + row).toggle(); } </script> <style> body { margin: 0 auto; padding: 0px; text-align: left; width: 100%; font-family: Helvetica, Arial, sans-serif; } #wrapper { margin: 0 auto; padding: 0px; text-align: left; width: 995px; } #wrapper  h1 { margin-top: 50px; font-size: 45px; color: #585858; } #wrapper h1 p { font-size: 20px; } #table_detail { width: 500px; text-align: left; border-collapse: collapse; color: #2E2E2E; border: #A4A4A4; } #table_detail tr:hover { background-color: #F2F2F2; } #table_detail .hidden_row { display: none; } </style>"""

    header = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>Test Report</title>          <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>       <style> tr:nth-of-type(odd) {{ background-color:#ccc; }} </style>        {scripty}          <style type="text/css" > .ansi2html-content {{ display: inline; white-space: pre-wrap; word-wrap: break-word; }} .body_foreground {{ color: #{page.config_parser['HTML_COLOR_THEME'].get('BODY_FOREGROUND_COLOR')}; }} .body_background {{ background-color: #{page.config_parser['HTML_COLOR_THEME'].get('BODY_BACKGROUND_COLOR')}; }} .inv_foreground {{ color: #{page.config_parser['HTML_COLOR_THEME'].get('INV_FOREGROUND_COLOR')}; }} .inv_background {{ background-color: #{page.config_parser['HTML_COLOR_THEME'].get('INV_BACKGROUND_COLOR')}; }} .ansi1 {{ font-weight: bold; }} .ansi31 {{ color: #aa0000; }} .ansi32 {{ color: #00aa00; }} .ansi33 {{ color: #aa5500; }} .ansi34 {{ color: #0000ff; }} .collapsible {{ font-weight: normal; color: #{page.config_parser['HTML_COLOR_THEME'].get('COLLAPSIBLE_FOREGROUND_COLOR')}; background-color: #{page.config_parser['HTML_COLOR_THEME'].get('COLLAPSIBLE_BACKGROUND_COLOR')}; cursor: pointer; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; }} .active, .collapsible:hover {{ foreground-color: #{page.config_parser['HTML_COLOR_THEME'].get('HOVER_FOREGROUND_COLOR')}; background-color: #{page.config_parser['HTML_COLOR_THEME'].get('HOVER_BACKGROUND_COLOR')}; color: white; }} .content {{ display: none; overflow: hidden; }} </style> </head> <body class="body_foreground body_background" style="font-size: normal; font-family: Helvetica, Arial, sans-serif;"> <pre class="ansi2html-content">"""

    metadata_button = f"""<div> <input type="button" id="meta_button" onclick="toggle_meta()" value="Show / Hide"/> </div> {page.metadata_table}"""
    metadata_script = """<script type="text/javascript"> const content = document.getElementById("metadata"); content.style.display = "none"; function toggle_meta() { if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } } </script>"""

    section_or_result_button_start = """<button type="button" class="collapsible">"""
    section_or_result_button_end = """</button> <div class="content"> <p>"""
    section_or_result_end = """</p> </div>"""
    section_or_result_button_script = """<script> var coll = document.getElementsByClassName("collapsible"); var i; for (i = 0; i < coll.length; i++) { coll[i].addEventListener("click", function() { this.classList.toggle("active"); var content = this.nextElementSibling; if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }); } </script>"""

    trailer = (
        """</pre>""" + section_or_result_button_script + """<hr> </body> </html>"""
    )

    html_out = (
        header
        + f"""<h2 style="font-family: Helvetica, Arial, sans-serif;">{HTML_OUTPUT_FILE.stem}</h2>"""
    )
    # html_out += sortable_css_js
    html_out += f"""<h4> Report generated on {datetime.now(timezone.utc).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')} UTC by pytest-tui version {__version__}</h4><hr>"""

    html_out += (
        """<h3 style="font-family: Helvetica, Arial, sans-serif;">Summary</h3>"""
    )
    html_out += page.clean(
        conv.convert(
            page.results.tui_sections.lastline.content.replace("=", "").strip(),
            full=False,
        )
    )
    html_out += """<hr>"""

    html_out += (
        """<h3 style="font-family: Helvetica, Arial, sans-serif;">Environment</h3>"""
    )
    html_out += f"""{metadata_button} {metadata_script} <hr>"""

    # Output Sections
    html_out += """<h3 style="font-family: Helvetica, Arial, sans-serif;">Output Sections</h3>"""
    for section in page.sections:
        html_out += (
            section_or_result_button_start + section + section_or_result_button_end
        )
        test = page.clean(conv.convert(page.sections[section], full=False))
        if not test:
            test = "No output"
        html_out += test + section_or_result_end
    html_out += """<hr>"""

    # Results Table
    page.create_results_table()
    html_out += """<h3 style="font-family: Helvetica, Arial, sans-serif;">Test Results (Sortable Table)</h3>\n"""
    html_out += (
        page.results_table + """<script> $('.sortable.table').tablesort(); </script>"""
    )

    # Results List
    html_out += """<h3 style="font-family: Helvetica, Arial, sans-serif;">Test Results (List)</h3>"""
    for result in page.results.tui_test_results.to_list():
        html_out += (
            section_or_result_button_start + result.fqtn + section_or_result_button_end
        )
        test = page.clean(
            conv.convert(
                result.caplog
                + result.capstderr
                + result.capstdout
                + result.longreprtext,
                full=False,
            )
        )
        if not test:
            test = "No output"
        html_out += test + section_or_result_end
    html_out += """<hr>"""

    # Final trailer and file write
    html_out += trailer
    with open(HTML_OUTPUT_FILE, "w+") as f:
        f.write(html_out)

    # Open in browser
    if page.config_parser["HTML"].get("html_autolaunch") == "True":
        webbrowser.open(f"file://{HTML_OUTPUT_FILE._str}")


if __name__ == "__main__":
    main()
