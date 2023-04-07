import pytest

WORKDIR = "/Users/jwr003/coding/pytest-tui"


@pytest.fixture(autouse=True)
def pom_vars():
    return {
        "TITLE": "Test Run Results",
        "ABOUT_TAB": "#defaultOpen",
        "ABOUT_TAB_FINAL_TEST_SUMMARY_BUTTON": "#About > button:nth-child(3)",
        "ABOUT_TAB_FINAL_TEST_SUMMARY_EXPANDED_TEXT": "short test summary info",
        "ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_BUTTON": "#About > button:nth-child(6)",
        "ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_1": "==",
        "ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_2": "collected",
        "ALL_TESTS_TAB": "body > div > span.tab > div > span:nth-child(2) > button",
        "ALL_TESTS_TAB_FIRST_TEST": "#All\ Tests > button:nth-child(1)",
        "ALL_TESTS_TAB_FIRST_TEST_RESULT": "#All\ Tests > div:nth-child(2) > pre",
        "FAILURES_TAB": "body > div > span.tab > div > span:nth-child(3) > button",
        "PASSES_TAB": "body > div > span.tab > div > span:nth-child(4) > button",
        "SKIPPED_TAB": "body > div > span.tab > div > span:nth-child(5) > button",
        "XFAILS_TAB": "body > div > span.tab > div > span:nth-child(6) > button",
        "XPASSES_TAB": "body > div > span.tab > div > span:nth-child(7) > button",
        "RERUNS_TAB": "body > div > span.tab > div > span:nth-child(8) > button",
        "FULL_OUTPUT_TAB": "body > div > span.tab > div > span:nth-child(11) > button",
        "FOLDED_OUTPUT_TAB": (
            "body > div > span.tab > div > span:nth-child(12) > button"
        ),
        "OUTPUT_SECTIONS_TAB": (
            "body > div > span.tab > div > span:nth-child(9) > button"
        ),
        "OUTPUT_SECTIONS_TAB_SUMMARY_SECTION": (
            "body > div > span.tab > div > span:nth-child(9) > span > span:nth-child(1)"
            " > button"
        ),
        "OUTPUT_SECTIONS_TAB_SUMMARY_SECTION_TEXT": "short test summary info",
        "OUTPUT_SECTIONS_TAB_FAILURES_SECTION": (
            "body > div > span.tab > div > span:nth-child(9) > span > span:nth-child(2)"
            " > button"
        ),
        "OUTPUT_SECTIONS_TAB_FAILURES_SECTION_TEXT": "= FAILURES =",
        "OUTPUT_SECTIONS_TAB_PASSES_SECTION": (
            "body > div > span.tab > div > span:nth-child(9) > span > span:nth-child(3)"
            " > button"
        ),
        "OUTPUT_SECTIONS_TAB_PASSES_SECTION_TEXT": "= PASSES =",
        "OUTPUT_SECTIONS_TAB_WARNINGS_SECTION": (
            "body > div > span.tab > div > span:nth-child(9) > span > span:nth-child(4)"
            " > button"
        ),
        "OUTPUT_SECTIONS_TAB_WARNINGS_SECTION_TEXT": "= warnings summary =",
        "OUTPUT_SECTIONS_TAB_ERRORS_SECTION": (
            "body > div > span.tab > div > span:nth-child(9) > span > span:nth-child(5)"
            " > button"
        ),
        "OUTPUT_SECTIONS_TAB_ERRORS_SECTION_TEXT": "= ERRORS =",
        "OUTPUT_SECTIONS_TAB_RERUNS_SECTION": (
            "body > div > span.tab > div > span:nth-child(9) > span > span:nth-child(6)"
            " > button"
        ),
        "OUTPUT_SECTIONS_TAB_RERUNS_SECTION_TEXT": "= rerun test summary info =",
        "FOLD_ACTIONS_TAB": "body > div > span.tab > div > span:nth-child(10) > button",
        "FOLD_ACTIONS_TAB_FOLD_UNFOLD_ACTION": (
            "body > div > span.tab > div > span:nth-child(10) > span >"
            " span:nth-child(1) > button"
        ),
        # "FOLD_ACTIONS_TAB_FOLD_UNFOLD_ACTION": "#toggle-details",
    }


def test_html_report_about_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['ABOUT_TAB']}:contains('About')")

    sb.assert_element(
        f"{pom_vars['ABOUT_TAB_FINAL_TEST_SUMMARY_BUTTON']}:contains('Final Test"
        " Summary')"
    )
    sb.assert_text_not_visible(pom_vars["ABOUT_TAB_FINAL_TEST_SUMMARY_EXPANDED_TEXT"])
    sb.click(pom_vars["ABOUT_TAB_FINAL_TEST_SUMMARY_BUTTON"])
    sb.assert_text_visible(pom_vars["ABOUT_TAB_FINAL_TEST_SUMMARY_EXPANDED_TEXT"])
    sb.click(pom_vars["ABOUT_TAB_FINAL_TEST_SUMMARY_BUTTON"])
    sb.assert_text_not_visible(pom_vars["ABOUT_TAB_FINAL_TEST_SUMMARY_EXPANDED_TEXT"])

    sb.assert_element(
        f"{pom_vars['ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_BUTTON']}:contains('Live Test"
        " Session Summary')"
    )
    sb.assert_text_not_visible(
        pom_vars["ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_1"]
    )
    sb.assert_text_not_visible(
        pom_vars["ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_2"]
    )
    sb.click(pom_vars["ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_BUTTON"])
    sb.assert_text_visible(
        pom_vars["ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_1"]
    )
    sb.assert_text_visible(
        pom_vars["ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_2"]
    )
    sb.click(pom_vars["ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_BUTTON"])
    sb.assert_text_not_visible(
        pom_vars["ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_1"]
    )
    sb.assert_text_not_visible(
        pom_vars["ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_2"]
    )

    sb.assert_element("#About > button:nth-child(9):contains('Test Execution Info')")
    sb.assert_text_visible("Test run started")
    sb.click(
        "#About > button:nth-child(9)",
    )
    sb.click(
        "#About > button:nth-child(9)",
    )
    sb.assert_text_not_visible("Test run started")
    sb.click(
        "#About > button:nth-child(9)",
    )
    sb.assert_text_visible("Test run started")

    sb.assert_element("#About > button:nth-child(12):contains('Environment')")
    sb.assert_text_visible("Plugins")
    sb.click(
        "#About > button:nth-child(12)",
    )
    sb.click(
        "#About > button:nth-child(12)",
    )
    sb.assert_text_not_visible("Plugins")
    sb.click(
        "#About > button:nth-child(12)",
    )
    sb.assert_text_visible("Plugins")


def test_html_report_all_tests_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['ALL_TESTS_TAB']}:contains('All Tests')")

    sb.click(f"{pom_vars['ALL_TESTS_TAB']}")
    sb.assert_element_not_visible(pom_vars["ALL_TESTS_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['ALL_TESTS_TAB_FIRST_TEST']}")
    sb.assert_element_visible(pom_vars["ALL_TESTS_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['ALL_TESTS_TAB_FIRST_TEST']}")
    sb.assert_element_not_visible(pom_vars["ALL_TESTS_TAB_FIRST_TEST_RESULT"])


def test_html_report_failures_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['FAILURES_TAB']}:contains('Failures')")


def test_html_report_test_passes_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['PASSES_TAB']}:contains('Passes')")


def test_html_report_test_skipped_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['SKIPPED_TAB']}:contains('Skipped')")


def test_html_report_test_xfails_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['XFAILS_TAB']}:contains('Xfails')")


def test_html_report_test_xpasses_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['XPASSES_TAB']}:contains('Xpasses')")


def test_html_report_test_reruns_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['RERUNS_TAB']}:contains('Reruns')")


def test_html_report_test_full_output_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['FULL_OUTPUT_TAB']}:contains('Full Output')")


def test_html_report_test_folded_output_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['FOLDED_OUTPUT_TAB']}:contains('Folded Output')")


def test_html_report_test_output_sections_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['OUTPUT_SECTIONS_TAB']}:contains('Output Sections')")

    sb.assert_element_not_visible(pom_vars["OUTPUT_SECTIONS_TAB_SUMMARY_SECTION"])
    sb.assert_element_not_visible(pom_vars["OUTPUT_SECTIONS_TAB_FAILURES_SECTION"])
    sb.assert_element_not_visible(pom_vars["OUTPUT_SECTIONS_TAB_PASSES_SECTION"])
    sb.assert_element_not_visible(pom_vars["OUTPUT_SECTIONS_TAB_WARNINGS_SECTION"])
    sb.assert_element_not_visible(pom_vars["OUTPUT_SECTIONS_TAB_ERRORS_SECTION"])
    sb.assert_element_not_visible(pom_vars["OUTPUT_SECTIONS_TAB_RERUNS_SECTION"])

    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB']}")
    sb.assert_element_visible(pom_vars["OUTPUT_SECTIONS_TAB_SUMMARY_SECTION"])
    sb.assert_element_visible(pom_vars["OUTPUT_SECTIONS_TAB_FAILURES_SECTION"])
    sb.assert_element_visible(pom_vars["OUTPUT_SECTIONS_TAB_PASSES_SECTION"])
    sb.assert_element_visible(pom_vars["OUTPUT_SECTIONS_TAB_WARNINGS_SECTION"])
    sb.assert_element_visible(pom_vars["OUTPUT_SECTIONS_TAB_ERRORS_SECTION"])
    sb.assert_element_visible(pom_vars["OUTPUT_SECTIONS_TAB_RERUNS_SECTION"])

    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB_SUMMARY_SECTION']}")
    sb.click(f"{pom_vars['OUTPUT_SECTIONS_TAB_SUMMARY_SECTION']}")
    sb.assert_text(pom_vars["OUTPUT_SECTIONS_TAB_SUMMARY_SECTION_TEXT"])

    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB']}")
    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB_FAILURES_SECTION']}")
    sb.click(f"{pom_vars['OUTPUT_SECTIONS_TAB_FAILURES_SECTION']}")
    sb.assert_text(pom_vars["OUTPUT_SECTIONS_TAB_FAILURES_SECTION_TEXT"])

    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB']}")
    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB_PASSES_SECTION']}")
    sb.click(f"{pom_vars['OUTPUT_SECTIONS_TAB_PASSES_SECTION']}")
    sb.assert_text(pom_vars["OUTPUT_SECTIONS_TAB_PASSES_SECTION_TEXT"])

    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB']}")
    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB_WARNINGS_SECTION']}")
    sb.click(f"{pom_vars['OUTPUT_SECTIONS_TAB_WARNINGS_SECTION']}")
    sb.assert_text(pom_vars["OUTPUT_SECTIONS_TAB_WARNINGS_SECTION_TEXT"])

    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB']}")
    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB_ERRORS_SECTION']}")
    sb.click(f"{pom_vars['OUTPUT_SECTIONS_TAB_ERRORS_SECTION']}")
    sb.assert_text(pom_vars["OUTPUT_SECTIONS_TAB_ERRORS_SECTION_TEXT"])

    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB']}")
    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB_RERUNS_SECTION']}")
    sb.click(f"{pom_vars['OUTPUT_SECTIONS_TAB_RERUNS_SECTION']}")
    sb.assert_text(pom_vars["OUTPUT_SECTIONS_TAB_RERUNS_SECTION_TEXT"])


def test_html_report_test_fold_actions_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.click(f"{pom_vars['FOLD_ACTIONS_TAB']}")
    sb.assert_text_visible("Folded")
    sb.click(f"{pom_vars['FOLD_ACTIONS_TAB']}")
    sb.assert_text_not_visible("Folded")
