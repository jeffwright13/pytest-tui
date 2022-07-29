import fire
import re
from pathlib import Path
from ansi2html import Ansi2HTMLConverter

MATCHER = r"(\x9B|\x1B\[)([0-?]*[ -\/]*[@-~])"

CODES_TO_HTML = {
    "0m": "</>",
    "1m": "<b>",
    "31m": "<p style='color:red;'>",
    "32m": "<p style='color:green;'>",
    "33m": "<p style='color:yellow;'>",
    "34m": "<p style='color:lue;'>",
    "35m": "<p style='color:magenta;'>",
    "36m": "<p style='color:cyan;'>",
    "37m": "<p style='color:white;'>",
    "38m": None,  # (256-color or RGB)
    "39m": "<p>",
    "39;49;00m": "</b>",
    "91m": "<b style='color:red;'>",
    "92m": "<b style='color:green;'>",
    "93m": "<b style='color:yellow;'>",
    "94m": "<b style='color:blue;'>",
    "95m": "<b style='color:magenta;'>",
    "96m": "<b style='color:cyan;'>",
    "97m": "<b style='color:white;'>",
}

HTML_HEADER = """
<!DOCTYPE html>
<html>
  <head>
    <title>Title of the document</title>
    <style>
      html * {
        font-size: 14px;
        line-height: 1.625;
        color: #2020131;
        font-family: Courier New;
      }
    </style>
  </head>
  <body>
"""

HTML_FOOTER = """
  </body>
</html>
"""

def replace_ansi_with_html(line: str) -> str:
    codes = re.findall(MATCHER, line)
    for code in codes:
        # result = re.search(code[0] + code[1], line)
        # print(f"Found {result.group()} at position {result.span()}")
        line = line.replace(code[0] + code[1], CODES_TO_HTML[code[1]], 1)
        line = (
            line.replace("\x1b[0m", "</p>", 1)
            if code[1][0] == "3"
            else line.replace("0m", "</b>", 1)
        )
    return line


def main(ansi_file: Path):
    with open(Path(ansi_file)) as f:
        lines = f.readlines()

    # converter = Ansi2HTMLConverter()
    # html = converter.convert("".join(lines))
    # with open(Path.cwd() / "testrun.html", "w") as outfile:
    #     outfile.write(html)

    # html = []
    # for line in lines:
    #     html.append(replace_ansi_with_html(line))
    # with open(Path.cwd() / "testrun.html", "w") as outfile:
    #     outfile.write(HTML_HEADER)
    #     for line in html:
    #         outfile.write(line)
    #     outfile.write(HTML_FOOTER)

    html = []
    html.append(replace_ansi_with_html(lines[-1]))
    with open(Path.cwd() / "testrun.html", "w") as outfile:
        outfile.write(HTML_HEADER)
        for line in html:
            outfile.write(line)
        outfile.write(HTML_FOOTER)



if __name__ == "__main__":
    fire.Fire(main)


"""
{'39;49;00m', '94m', '33m', '1m', '31m', '37m', '35m', '0m', '92m', '96m', '32m'}
Per https://en.wikipedia.org/wiki/ANSI_escape_code#SGR, these are:
39: Default foreground color; 49: Default background color; 00m: Reset
1m: Bold
92m: bright green
96m: bright cyan
94m: Set bright foreground color (blue)
31m: Set foreground color (red)
32m: Set foreground color (green)
33m: Set foreground color (yellow)
34m: Set foreground color (blue)
35m: Set foreground color (magenta)
36m: Set foreground color (cyan)
37m: Set foreground color (white)
{'94m', '39;49;00m', '33m', '92m', '1m', '31m', '37m', '96m', '35m', '0m', '32m'}
"""
