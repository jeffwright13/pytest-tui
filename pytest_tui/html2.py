import json
import re
import webbrowser

import json2table
from ansi2html import Ansi2HTMLConverter
from strip_ansi import strip_ansi

TABS = (
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
)


class HtmlPage:
    def __init__(
        self,
    ):
        pass

    def create_header(self) -> str:
        return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <title>html_report</title> </head> <body class="body_foreground body_background" style="font-size: normal;" > <pre class="ansi2html-content">"""

    def create_trailer(self) -> str:
        return """</pre> </body> </html>"""

    def create_tabs(self) -> str:
        tabs_links = [
            f"""<button class="tablinks" onclick="openCity(event, '{tab}')">{tab}</button>"""
            for tab in TABS
        ]
        tab_links_section = """<div class="tab">""" + "".join(tabs_links) + """</div>"""
        tab_content = [
            f"""<div id="{tab}" class="tabcontent"> <h3>{tab}</h3> <p>{tab} content.</p> </div>"""
            for tab in TABS
        ]
        tab_content_section = "".join(tab_content)
        return tab_links_section + tab_content_section

    def create_js(self) -> str:
        return """<script> function openCity(evt, cityName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(cityName).style.display = "block"; evt.currentTarget.className += " active"; } </script>"""

def main():  # sourcery skip: low-code-quality, use-fstring-for-concatenation
    conv = Ansi2HTMLConverter()
    page = HtmlPage()
    html_header = page.create_header()
    html_tabs = page.create_tabs()
    html_js = page.create_js()
    html_trailer = page.create_trailer()

    html_out = html_header + html_tabs + html_js + html_trailer

    with open("html2.html", "w+") as f:
        f.write(html_out)
    pass

if __name__ == "__main__":
    main()
