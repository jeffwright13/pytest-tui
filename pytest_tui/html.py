import os
import re
import time
import webbrowser

from ansi2html import Ansi2HTMLConverter

from pytest_tui import __version__
from pytest_tui.utils import HTMLOUTPUTFILE, Results

BODY_FOREGROUND_COLOR = "AAAAAA"
BODY_BACKGROUND_COLOR = "000000"
INV_FOREGROUND_COLOR = "000000"
INV_BACKGROUND_COLOR = "AAAAAA"
COLLAPSIBLE_FOREGROUND_COLOR = "AAAAAA"
COLLAPSIBLE_BACKGROUND_COLOR = "000000"
HOVER_FOREGROUND_COLOR = "111111"
HOVER_BACKGROUND_COLOR = "999999"


class HtmlPage:
    def __init__(
        self,
    ):
        self.results = Results()
        self.sections = {
            "Start": self.results.Sections["TEST_SESSION_STARTS"].content,
            "Summary": self.results.Sections["LAST_LINE"].content
            + self.results.Sections["SHORT_TEST_SUMMARY"].content,
            "Warnings": self.results.Sections["WARNINGS_SUMMARY"].content,
            "Rerun": self.results.Sections["RERUN_SUMMARY"].content,
            "Errors": self.results.Sections["ERRORS_SECTION"].content,
            "Full Output": self.results.unmarked_output,
        }
        self.summary = self.results.Sections["LAST_LINE"].content.replace("=", "")


def clean(text: str) -> str:
    return re.sub("\\n+", "\\n", text)


def main(autolaunch: bool = True):  # sourcery skip: low-code-quality, use-fstring-for-concatenation
    conv = Ansi2HTMLConverter()
    page = HtmlPage()

    header = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>Test Report</title> <style type="text/css"> .ansi2html-content {{ display: inline; white-space: pre-wrap; word-wrap: break-word; }} .body_foreground {{ color: #{BODY_FOREGROUND_COLOR}; }} .body_background {{ background-color: #{BODY_BACKGROUND_COLOR}; }} .inv_foreground {{ color: #{INV_FOREGROUND_COLOR}; }} .inv_background {{ background-color: #{INV_BACKGROUND_COLOR}; }} .ansi1 {{ font-weight: bold; }} .ansi31 {{ color: #aa0000; }} .ansi32 {{ color: #00aa00; }} .ansi33 {{ color: #aa5500; }} .collapsible {{ font-weight: bold; color: #{COLLAPSIBLE_FOREGROUND_COLOR}; background-color: #{COLLAPSIBLE_BACKGROUND_COLOR}; cursor: pointer; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; }} .active, .collapsible:hover {{ foreground-color: #{HOVER_FOREGROUND_COLOR}; background-color: #{HOVER_BACKGROUND_COLOR}; /* Green */ color: white; }} .content {{ display: none; overflow: hidden; }} </style> </head> <body class="body_foreground body_background" style="font-size: normal;"> <pre class="ansi2html-content">"""

    button_start = """<button type="button" class="collapsible">"""
    button_end = """</button> <div class="content"> <p>"""
    test_end = """</p> </div>"""

    script = """<script> var coll = document.getElementsByClassName("collapsible"); var i; for (i = 0; i < coll.length; i++) { coll[i].addEventListener("click", function() { this.classList.toggle("active"); var content = this.nextElementSibling; if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }); } </script>"""

    trailer = """</pre>""" + script + """</body> </html>"""

    html_out = header + "<h1>report.html</h1 s>"
    html_out += clean(
        conv.convert(
            page.results.Sections["LAST_LINE"].content.replace("=", "").strip(),
            full=False,
        )
    )
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(
        HTMLOUTPUTFILE
    )
    html_out += f"<p>Report generated on {time.ctime(mtime)} by pytest-tui version {__version__}</p>"

    # Sections
    for section in page.sections:
        html_out += "<hr> <h3>" + section.upper() + "</h3>"
        html_out += button_start + section + button_end
        test = clean(conv.convert(page.sections[section], full=False))
        if not test:
            test = "<p>No output</p>"
        html_out += test + test_end

    # Test Results
    for result in ["failures", "passes", "skipped", "errors", "xpasses", "xfails"]:
        html_out += "<hr> <p> <b>" + result.upper() + "</b> </p>"
        nodes = eval(f"page.results.tests_{result}")
        if nodes:
            for node in nodes:
                html_out += button_start + node + button_end
                test = clean(
                    conv.convert(eval(f"page.results.tests_{result}[node]"), full=False)
                )
                if not test:
                    test = "<p>No output</p>"
                html_out += test + test_end

    # Final trailer and file write
    html_out += trailer
    with open(HTMLOUTPUTFILE, "w") as f:
        f.write(html_out)

    # Open in browser
    if autolaunch:
        webbrowser.open(f"file://{HTMLOUTPUTFILE._str}")


if __name__ == "__main__":
    main()
