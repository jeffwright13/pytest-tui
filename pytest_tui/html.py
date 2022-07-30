from pytest_tui.utils import Results
from ansi2html import Ansi2HTMLConverter
from pytest_tui.utils import HTMLOUTPUTFILE
from pytest_tui import __version__

import os
import re
import time


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
            "Errors": self.results.Sections["ERRORS_SECTION"].content,
            "Full Output": self.results.unmarked_output,
        }
        self.summary = self.results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )

def clean(text: str) -> str:
    return re.sub("\\n+", "\\n", text)

def main():  # sourcery skip: low-code-quality, use-fstring-for-concatenation
    conv = Ansi2HTMLConverter()
    page = HtmlPage()

    header = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>Test Report</title> <style type="text/css"> .ansi2html-content { display: inline; white-space: pre-wrap; word-wrap: break-word; } .body_foreground { color: #AAAAAA; } .body_background { background-color: #000000; } .inv_foreground { color: #000000; } .inv_background { background-color: #AAAAAA; } .ansi1 { font-weight: bold; } .ansi31 { color: #aa0000; } .ansi32 { color: #00aa00; } .ansi33 { color: #aa5500; } .collapsible { font-weight: bold; color: #AAAAAA; background-color: #000000; cursor: pointer; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; } .active, .collapsible:hover { } .content {  display: none; overflow: hidden; } </style> </head> <body class="body_foreground body_background" style="font-size: normal;"> <pre class="ansi2html-content">"""

    button_start = """<button type="button" class="collapsible">"""
    button_end = """</button> <div class="content"> <p>"""
    test_end = """</p> </div>"""

    script = """<script> var coll = document.getElementsByClassName("collapsible"); var i; for (i = 0; i < coll.length; i++) { coll[i].addEventListener("click", function() { this.classList.toggle("active"); var content = this.nextElementSibling; if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }); } </script>"""

    trailer = """</pre>""" + script + """</body> </html>"""

    html_out = header + "<h1>report.html</h1 s>"

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(HTMLOUTPUTFILE)
    html_out += f"<p>Report generated on {time.ctime(mtime)} by pytest-tui version {__version__}</p>"

    # html_out += clean(conv.convert(page.results.Sections["LAST_LINE"].content))

    # Sections
    html_out += "<hr><p><b>" + "TEST SESSION START" + "</b></p>"
    html_out += button_start + "Test Session Start" + button_end
    test = clean(conv.convert(page.sections["Start"]))
    if not test: test = "<p>No output</p>"
    html_out += test + test_end

    html_out += "<hr><p><b>" + "SUMMARY" + "</b></p>"
    html_out += button_start + "Summary" + button_end
    test = clean(conv.convert(page.sections["Summary"]))
    if not test: test = "<p>No output</p>"
    html_out += test + test_end

    html_out += "<hr><p><b>" + "WARNINGS" + "</b></p>"
    html_out += button_start + "Warnings" + button_end
    test = clean(conv.convert(page.sections["Warnings"]))
    if not test: test = "<p>No output</p>"
    html_out += test + test_end

    html_out += "<hr><p><b>" + "ERRORS" + "</b></p>"
    html_out += button_start + "Errors" + button_end
    test = clean(conv.convert(page.sections["Errors"]))
    if not test: test = "<p>No output</p>"
    html_out += test + test_end

    html_out += "<hr><p><b>" + "FULL OUTPUT" + "</b></p>"
    html_out += button_start + "Full Output" + button_end
    test = clean(conv.convert(page.sections["Full Output"]))
    if not test: test = "<p>No output</p>"
    html_out += test + test_end

    html_out += "<hr><p><b>" + "FAILURES" + "</b></p>"
    for node in page.results.tests_failures:
        html_out +=  button_start + node + button_end
        test = clean(conv.convert(page.results.tests_failures[node], full=False))
        if not test: test = "<p>No output</p>"
        html_out += test + test_end

    html_out += "<hr><p><b>" + "PASSES" + "</b></p>"
    for node in page.results.tests_passes:
        html_out +=  button_start + node + button_end
        test = clean(conv.convert(page.results.tests_passes[node], full=False))
        if not test: test = "<p>No output</p>"
        html_out += test + test_end

    html_out += "<hr><p><b>" + "SKIPPED" + "</b></p>"
    for node in page.results.tests_skipped:
        html_out +=  button_start + node + button_end
        test = clean(conv.convert(page.results.tests_skipped[node], full=False))
        if not test: test = "<p>No output</p>"
        html_out += test + test_end

    html_out += "<hr><p><b>" + "ERRORS" + "</b></p>"
    for node in page.results.tests_errors:
        html_out +=  button_start + node + button_end
        test = clean(conv.convert(page.results.tests_errors[node], full=False))
        html_out += test + test_end

    html_out += "<hr><p><b>" + "XPASSES" + "</b></p>"
    for node in page.results.tests_xpasses:
        html_out +=  button_start + node + button_end
        test = clean(conv.convert(page.results.tests_xpasses[node], full=False))
        if not test: test = "<p>No output</p>"
        html_out += test + test_end

    html_out += "<hr><p><b>" + "XFAILS" + "</b></p>"
    for node in page.results.tests_xfails:
        html_out +=  button_start + node + button_end
        test = clean(conv.convert(page.results.tests_xfails[node], full=False))
        if not test: test = "<p>No output</p>"
        html_out += test + test_end

    # Final trailer and file write
    html_out += trailer
    with open(HTMLOUTPUTFILE, "w") as f:
        f.write(html_out)


if __name__ == "__main__":
    main()
