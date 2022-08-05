import os
import re
import time
import webbrowser

from ansi2html import Ansi2HTMLConverter

from pytest_tui import __version__
from pytest_tui.utils import HTMLOUTPUTFILE, Results


class HtmlPage:
    def __init__(
        self,
    ):
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


def clean(text: str) -> str:
    return re.sub("\\n+", "\\n", text)


def main(autolaunch: bool = True, dark: bool = False):  # sourcery skip: low-code-quality, use-fstring-for-concatenation

    if dark:
        BODY_FOREGROUND_COLOR = "AAAAAA"
        BODY_BACKGROUND_COLOR = "000000"
        INV_FOREGROUND_COLOR = "000000"
        INV_BACKGROUND_COLOR = "AAAAAA"
        COLLAPSIBLE_FOREGROUND_COLOR = "AAAAAA"
        COLLAPSIBLE_BACKGROUND_COLOR = "000000"
        HOVER_FOREGROUND_COLOR = "111111"
        HOVER_BACKGROUND_COLOR = "999999"
    else:
        BODY_FOREGROUND_COLOR = "000000"
        BODY_BACKGROUND_COLOR = "EEEEEE"
        INV_FOREGROUND_COLOR = "000000"
        INV_BACKGROUND_COLOR = "AAAAAA"
        COLLAPSIBLE_FOREGROUND_COLOR = "000000"
        COLLAPSIBLE_BACKGROUND_COLOR = "EEEEEE"
        HOVER_FOREGROUND_COLOR = "EEEEEE"
        HOVER_BACKGROUND_COLOR = "000000"


    conv = Ansi2HTMLConverter()
    page = HtmlPage()

    header = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>Test Report</title> <style type="text/css"> .ansi2html-content {{ display: inline; white-space: pre-wrap; word-wrap: break-word; }} .body_foreground {{ color: #{BODY_FOREGROUND_COLOR}; }} .body_background {{ background-color: #{BODY_BACKGROUND_COLOR}; }} .inv_foreground {{ color: #{INV_FOREGROUND_COLOR}; }} .inv_background {{ background-color: #{INV_BACKGROUND_COLOR}; }} .ansi1 {{ font-weight: bold; }} .ansi31 {{ color: #aa0000; }} .ansi32 {{ color: #00aa00; }} .ansi33 {{ color: #aa5500; }} .collapsible {{ font-weight: bold; color: #{COLLAPSIBLE_FOREGROUND_COLOR}; background-color: #{COLLAPSIBLE_BACKGROUND_COLOR}; cursor: pointer; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; }} .active, .collapsible:hover {{ foreground-color: #{HOVER_FOREGROUND_COLOR}; background-color: #{HOVER_BACKGROUND_COLOR}; /* Green */ color: white; }} .content {{ display: none; overflow: hidden; }} </style> </head> <body class="body_foreground body_background" style="font-size: normal;"> <pre class="ansi2html-content">"""

    environ = """<table id="environment"> <tr> <td>GEMS Account Server Version</td> <td>6.0.1</td></tr> <tr> <td>GEMS Core Version</td> <td>5.14.0</td></tr> <tr> <td>GEMS Project Version</td> <td>36</td></tr> <tr> <td>GEMS REST Server Version</td> <td>5.19.4</td></tr> <tr> <td>GEMS Site Name</td> <td>Zenith Tanami</td></tr> <tr> <td>GEMS Site Timezone</td> <td>UTC</td></tr> <tr> <td>JAVA_HOME</td> <td>/Users/jwr003/Library/Java/JavaVirtualMachines/corretto-11.0.12/Contents/Home</td></tr> <tr> <td>Packages</td> <td>{"pluggy": "0.13.1", "py": "1.11.0", "pytest": "6.2.5"}</td></tr> <tr> <td>Platform</td> <td>macOS-12.4-x86_64-i386-64bit</td></tr> <tr> <td>Plugins</td> <td>{"Faker": "13.15.1", "automock": "0.8.0", "bdd": "5.0.0", "cov": "3.0.0", "forked": "1.4.0", "html": "3.1.1", "metadata": "2.0.1", "mock": "3.8.1", "mock-generator": "1.2.0", "pytest_check": "1.0.5", "repeat": "0.9.1", "rerunfailures": "10.2", "timeout": "2.1.0", "tui": "1.0.1", "xdist": "2.5.0"}</td></tr> <tr> <td>Python</td>"""

    environ_script = """<div><input type="button" id="env_button" onclick="toggle_env()" value="Show Environment" /></div> </div> <script type="text/javascript"> function toggle_env() { var x = document.getElementById("environment"); if (x.style.display === "block") { x.style.display = "none"; } else { x.style.display = "block"; } } </script>"""

    button_start = """<button type="button" class="collapsible">"""
    button_end = """</button> <div class="content"> <p>"""
    test_end = """</p> </div>"""

    script = """<script> var coll = document.getElementsByClassName("collapsible"); var i; for (i = 0; i < coll.length; i++) { coll[i].addEventListener("click", function() { this.classList.toggle("active"); var content = this.nextElementSibling; if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }); } </script>"""

    trailer = """</pre>""" + script + """</body> </html>"""

    html_out = header + f"<h1>{HTMLOUTPUTFILE.stem}</h1 s>"
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
    html_out += environ + environ_script

    # Sections
    html_out +=  "<hr> <h2>" + "OUTPUT SECTIONS" + "</h2>"
    for section in page.sections:
        # html_out += "<hr> <h2>" + section.upper() + "</h2>"
        html_out +=  button_start + section + button_end
        test = clean(conv.convert(page.sections[section], full=False))
        if not test:
            test = "<p>No output</p>"
        html_out += test + test_end

    # Test Results
    html_out +=  "<hr> <h2>" + "INDIVIDUAL TEST RESULTS" + "</h2>"
    for result in ["failures", "passes", "skipped", "errors", "xpasses", "xfails"]:
        html_out += "<h3>" + result.title() + "</h3>"
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
    with open(HTMLOUTPUTFILE, "w+") as f:
        f.write(html_out)

    # Open in browser
    if autolaunch:
        webbrowser.open(f"file://{HTMLOUTPUTFILE._str}")


if __name__ == "__main__":
    main()
