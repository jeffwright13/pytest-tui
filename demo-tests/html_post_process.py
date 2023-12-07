import re
import sys


def post_process_html_report(html_report_path):
    with open(html_report_path, "r", encoding="utf-8") as file:
        content = file.read()

    # This regex pattern needs to match the log output format precisely
    pattern = re.compile(
        r"\[DETAILS\](.*?)\[SUMMARY\](.*?)\[/SUMMARY\](.*?)\[/DETAILS\]", re.DOTALL
    )

    # Replace the pattern with the HTML details/summary tags
    def replace_with_tags(match):
        return f"<details><summary>{match.group(2)}</summary>{match.group(3)}</details>"

    content = pattern.sub(replace_with_tags, content)

    with open(html_report_path, "w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    # Check for command line arguments for the report path
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_html_report>")
        sys.exit(1)

    report_path = sys.argv[1]
    post_process_html_report(report_path)
