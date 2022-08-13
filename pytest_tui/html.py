import configparser
import json
import re
import webbrowser
from datetime import datetime, timezone

import json2table
from ansi2html import Ansi2HTMLConverter
from strip_ansi import strip_ansi

from pytest_tui import __version__
from pytest_tui.__main__ import Cli
from pytest_tui.utils import CONFIGFILE, HTMLOUTPUTFILE, OUTCOMES, Results


class HtmlPage:
    def __init__(
        self,
    ):
        self.config_parser = configparser.ConfigParser()
        try:
            self.config_parser.read(CONFIGFILE)
        except Exception:
            Cli().apply_default_config()
            self.config_parser.read(CONFIGFILE)

        self.results = Results()
        self.sections = {
            "test session starts": self.results.Sections["TEST_SESSION_STARTS"].content,
            "short test summary info": self.results.Sections["LAST_LINE"].content
            + self.results.Sections["SHORT_TEST_SUMMARY"].content,
            "warnings summary": self.results.Sections["WARNINGS_SUMMARY"].content,
            "rerun test summary info": self.results.Sections["RERUN_SUMMARY"].content,
            "errors": self.results.Sections["ERRORS_SECTION"].content,
            "full output": self.results.unmarked_output,
        }
        self.summary = self.results.Sections["LAST_LINE"].content.replace("=", "")

    def read_environment(self) -> None:
        e = strip_ansi(self.results.Sections["TEST_SESSION_STARTS"].content).split(
            "\n"
        )[1:]
        idx = e.index("collecting ... ")
        self.environment = e[:idx]

    def create_meta_table(self) -> None:
        self.read_environment()
        self.metadata = json.loads(
            [line for line in self.environment if "metadata:" in line][0]
            .lstrip("metadata: ")
            .replace("'", '"')
        )
        self.metadata.pop("JAVA_HOME")
        self.metadata_table = json2table.convert(
            self.metadata,
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


def main():  # sourcery skip: low-code-quality, use-fstring-for-concatenation

    conv = Ansi2HTMLConverter()
    page = HtmlPage()
    page.create_meta_table()

    header = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>Test Report</title> <style type="text/css" > .ansi2html-content {{ display: inline; white-space: pre-wrap; word-wrap: break-word; }} .body_foreground {{ color: #{page.config_parser['HTML_COLOR_THEME'].get('BODY_FOREGROUND_COLOR')}; }} .body_background {{ background-color: #{page.config_parser['HTML_COLOR_THEME'].get('BODY_BACKGROUND_COLOR')}; }} .inv_foreground {{ color: #{page.config_parser['HTML_COLOR_THEME'].get('INV_FOREGROUND_COLOR')}; }} .inv_background {{ background-color: #{page.config_parser['HTML_COLOR_THEME'].get('INV_BACKGROUND_COLOR')}; }} .ansi1 {{ font-weight: bold; }} .ansi31 {{ color: #aa0000; }} .ansi32 {{ color: #00aa00; }} .ansi33 {{ color: #aa5500; }} .ansi34 {{ color: #0000ff; }} .collapsible {{ font-weight: normal; color: #{page.config_parser['HTML_COLOR_THEME'].get('COLLAPSIBLE_FOREGROUND_COLOR')}; background-color: #{page.config_parser['HTML_COLOR_THEME'].get('COLLAPSIBLE_BACKGROUND_COLOR')}; cursor: pointer; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; }} .active, .collapsible:hover {{ foreground-color: #{page.config_parser['HTML_COLOR_THEME'].get('HOVER_FOREGROUND_COLOR')}; background-color: #{page.config_parser['HTML_COLOR_THEME'].get('HOVER_BACKGROUND_COLOR')}; color: white; }} .content {{ display: none; overflow: hidden; }} </style> </head> <body class="body_foreground body_background" style="font-size: normal; font-family: monospace, monospace;"> <pre class="ansi2html-content">"""

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
        + f"""<h2 style="font-family: Helvetica, Arial, sans-serif;">{HTMLOUTPUTFILE.stem}</h2>"""
    )
    html_out += f"""<h4> Report generated on {datetime.now(timezone.utc).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')} UTC by pytest-tui version {__version__}</h4><hr>"""

    html_out += (
        """<h3 style="font-family: Helvetica, Arial, sans-serif;">Summary</h3>"""
    )
    html_out += page.clean(
        conv.convert(
            page.results.Sections["LAST_LINE"].content.replace("=", "").strip(),
            full=False,
        )
    )
    html_out += """<hr>"""

    html_out += (
        """<h3 style="font-family: Helvetica, Arial, sans-serif;">Environment</h3>"""
    )
    html_out += f"""{metadata_button} {metadata_script} <hr>"""

    # Sections
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

    # Test Results By Outcome
    html_out += """<h3 style="font-family: Helvetica, Arial, sans-serif;">Test Results By Outcome</h3>"""
    for outcome in OUTCOMES:
        html_out += f"""<h4 style="font-family: Helvetica, Arial, sans-serif;">{outcome.title()} </h4>"""
        nodes = eval(f"page.results.tests_{outcome.lower()}")
        if nodes:
            for node in nodes:
                html_out += f"""{section_or_result_button_start}{node}{section_or_result_button_end}"""
                test = f"""<p>{page.clean(
                    conv.convert(eval(f"page.results.tests_{outcome.lower()}[node]"), full=False)
                )}</p>"""
                if not test:
                    test = "<p>No output</p>"
                html_out += test + section_or_result_end
    html_out += """<hr>"""

    # Test Results in Order of Execution
    html_out += """<h3 style="font-family: Helvetica, Arial, sans-serif;">Test Results in Order of Execution</h3>"""
    for testname, result in page.results.OutcomesChronological.items():
        html_out += f"""<tr><td>{section_or_result_button_start}<b>{result}</b>      {testname}{section_or_result_button_end}</td></tr>"""
        test = page.clean(
            conv.convert(eval(f"page.results.tests_all['{testname}']"), full=False)
        )
        if not test:
            test = "<p>No output</p>"
        html_out += test + section_or_result_end

    # Final trailer and file write
    html_out += trailer
    with open(HTMLOUTPUTFILE, "w+") as f:
        f.write(html_out)

    # Open in browser
    if page.config_parser["HTML"].get("autolaunch_html") == "True":
        webbrowser.open(f"file://{HTMLOUTPUTFILE._str}")


if __name__ == "__main__":
    main()
