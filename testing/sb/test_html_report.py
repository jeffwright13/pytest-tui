import pytest

WORKDIR = "/Users/jwr003/coding/pytest-tui"


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

    sb.assert_element(pom_vars["ABOUT_TAB_TEST_EXECUTION_INFO_BUTTON"])
    sb.assert_text_visible(pom_vars["ABOUT_TAB_TEST_EXECUTION_INFO_EXPANDED_TEXT"])
    sb.click(pom_vars["ABOUT_TAB_TEST_EXECUTION_INFO_BUTTON"])
    sb.click(pom_vars["ABOUT_TAB_TEST_EXECUTION_INFO_BUTTON"])
    sb.assert_text_not_visible(pom_vars["ABOUT_TAB_TEST_EXECUTION_INFO_EXPANDED_TEXT"])
    sb.click(pom_vars["ABOUT_TAB_TEST_EXECUTION_INFO_BUTTON"])
    sb.assert_text_visible(pom_vars["ABOUT_TAB_TEST_EXECUTION_INFO_EXPANDED_TEXT"])

    sb.assert_element(pom_vars["ABOUT_TAB_ENVIRONMENT_BUTTON"])
    sb.assert_text_visible(pom_vars["ABOUT_TAB_ENVIRONMENT_EXPANDED_TEXT"])
    sb.click(pom_vars["ABOUT_TAB_ENVIRONMENT_BUTTON"])
    sb.click(pom_vars["ABOUT_TAB_ENVIRONMENT_BUTTON"])
    sb.assert_text_not_visible(pom_vars["ABOUT_TAB_ENVIRONMENT_EXPANDED_TEXT"])
    sb.click(pom_vars["ABOUT_TAB_ENVIRONMENT_BUTTON"])
    sb.assert_text_visible(pom_vars["ABOUT_TAB_ENVIRONMENT_EXPANDED_TEXT"])


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
    sb.click(f"{pom_vars['FAILURES_TAB']}")
    sb.assert_element_not_visible(pom_vars["FAILURES_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['FAILURES_TAB_FIRST_TEST']}")
    sb.assert_element_visible(pom_vars["FAILURES_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['FAILURES_TAB_FIRST_TEST']}")
    sb.assert_element_not_visible(pom_vars["FAILURES_TAB_FIRST_TEST_RESULT"])


def test_html_report_test_passes_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['PASSES_TAB']}:contains('Passes')")
    sb.click(f"{pom_vars['PASSES_TAB']}")
    sb.assert_element_not_visible(pom_vars["PASSES_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['PASSES_TAB_FIRST_TEST']}")
    sb.assert_element_visible(pom_vars["PASSES_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['PASSES_TAB_FIRST_TEST']}")
    sb.assert_element_not_visible(pom_vars["PASSES_TAB_FIRST_TEST_RESULT"])


def test_html_report_test_skipped_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['SKIPPED_TAB']}:contains('Skipped')")
    sb.click(f"{pom_vars['SKIPPED_TAB']}")
    sb.assert_element_not_visible(pom_vars["SKIPPED_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['SKIPPED_TAB_FIRST_TEST']}")
    sb.assert_element_visible(pom_vars["SKIPPED_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['SKIPPED_TAB_FIRST_TEST']}")
    sb.assert_element_not_visible(pom_vars["SKIPPED_TAB_FIRST_TEST_RESULT"])


def test_html_report_test_xfails_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['XFAILS_TAB']}:contains('Xfails')")
    sb.click(f"{pom_vars['XFAILS_TAB']}")
    sb.assert_element_not_visible(pom_vars["XFAILS_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['XFAILS_TAB_FIRST_TEST']}")
    sb.assert_element_visible(pom_vars["XFAILS_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['XFAILS_TAB_FIRST_TEST']}")
    sb.assert_element_not_visible(pom_vars["XFAILS_TAB_FIRST_TEST_RESULT"])


def test_html_report_test_xpasses_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['XPASSES_TAB']}:contains('Xpasses')")
    sb.click(f"{pom_vars['XPASSES_TAB']}")
    sb.assert_element_not_visible(pom_vars["XPASSES_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['XPASSES_TAB_FIRST_TEST']}")
    sb.assert_element_visible(pom_vars["XPASSES_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['XPASSES_TAB_FIRST_TEST']}")
    sb.assert_element_not_visible(pom_vars["XPASSES_TAB_FIRST_TEST_RESULT"])


def test_html_report_test_reruns_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['RERUNS_TAB']}:contains('Reruns')")
    sb.click(f"{pom_vars['RERUNS_TAB']}")
    sb.assert_element_not_visible(pom_vars["RERUNS_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['RERUNS_TAB_FIRST_TEST']}")
    sb.assert_element_visible(pom_vars["RERUNS_TAB_FIRST_TEST_RESULT"])
    sb.click(f"{pom_vars['RERUNS_TAB_FIRST_TEST']}")
    sb.assert_element_not_visible(pom_vars["RERUNS_TAB_FIRST_TEST_RESULT"])


def test_html_report_test_full_output_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.assert_title(pom_vars["TITLE"])
    sb.assert_element(f"{pom_vars['FULL_OUTPUT_TAB']}:contains('Full Output')")
    sb.click(f"{pom_vars['FULL_OUTPUT_TAB']}")
    sb.assert_element(
        f"{pom_vars['FULL_OUTPUT_TAB_EXPANDED_TEXT']}:contains('== test session starts"
        " ==')"
    )
    sb.assert_element(
        f"{pom_vars['FULL_OUTPUT_TAB_EXPANDED_TEXT']}:contains('== ERRORS ==')"
    )
    sb.assert_element(
        f"{pom_vars['FULL_OUTPUT_TAB_EXPANDED_TEXT']}:contains('== FAILURES ==')"
    )
    sb.assert_element(
        f"{pom_vars['FULL_OUTPUT_TAB_EXPANDED_TEXT']}:contains('== PASSES ==')"
    )
    sb.assert_element(
        f"{pom_vars['FULL_OUTPUT_TAB_EXPANDED_TEXT']}:contains('== short test summary"
        " info ==')"
    )
    sb.assert_element(
        f"{pom_vars['FULL_OUTPUT_TAB_EXPANDED_TEXT']}:contains('== rerun test summary"
        " info ==')"
    )


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
    sb.click(f"{pom_vars['OUTPUT_SECTIONS_TAB_ERRORS_SECTION']}")
    sb.assert_text(pom_vars["OUTPUT_SECTIONS_TAB_ERRORS_SECTION_TEXT"])

    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB']}")
    sb.hover(f"{pom_vars['OUTPUT_SECTIONS_TAB_RERUNS_SECTION']}")
    sb.click(f"{pom_vars['OUTPUT_SECTIONS_TAB_RERUNS_SECTION']}")
    sb.assert_text(pom_vars["OUTPUT_SECTIONS_TAB_RERUNS_SECTION_TEXT"])


def test_html_report_test_fold_actions_tab(sb, pom_vars: dict[str, str]):
    sb.open(f"file:///{WORKDIR}/ptt_files/html_report.html")
    sb.click(pom_vars["FOLDED_OUTPUT_TAB"])
    sb.scroll_into_view("Summary", by="tag name")
    sb.assert_element_not_visible(pom_vars["FOLD_ACTIONS_TAB_FOLD_UNFOLD_ACTION"])
    sb.assert_element_not_visible(pom_vars["FOLD_ACTIONS_TAB_SHOW_HIDE_ACTION"])
    sb.hover(f"{pom_vars['FOLD_ACTIONS_TAB']}")
    sb.find_element(pom_vars["FOLD_ACTIONS_TAB_FOLD_UNFOLD_ACTION"])
    sb.assert_element_visible(pom_vars["FOLD_ACTIONS_TAB_FOLD_UNFOLD_ACTION"])
    sb.find_element(pom_vars["FOLD_ACTIONS_TAB_SHOW_HIDE_ACTION"])
    sb.assert_element_visible(pom_vars["FOLD_ACTIONS_TAB_SHOW_HIDE_ACTION"])
    sb.click(pom_vars["FOLD_ACTIONS_TAB_FOLD_UNFOLD_ACTION"])
    sb.wait_for_element_clickable("Summary", by="tag name")
    sb.click(pom_vars["FOLD_ACTIONS_TAB_SHOW_HIDE_ACTION"])
    sb.click(pom_vars["FOLD_ACTIONS_TAB_SHOW_HIDE_ACTION"])
    sb.wait_for_element_not_visible("Summary", by="tag name")
