import pytest


@pytest.fixture
def pom_vars():
    return {
        "TITLE": "Test Run Results",
        "ABOUT_TAB": "#defaultOpen",
        "ABOUT_TAB_FINAL_TEST_SUMMARY_BUTTON": "#About > button:nth-child(3)",
        "ABOUT_TAB_FINAL_TEST_SUMMARY_EXPANDED_TEXT": "short test summary info",
        "ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_BUTTON": "#About > button:nth-child(6)",
        "ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_1": "==",
        "ABOUT_TAB_LIVE_TEST_SESSION_SUMMARY_EXPANDED_TEXT_2": "collected",
        "ABOUT_TAB_TEST_EXECUTION_INFO_BUTTON": "#About > button:nth-child(9)",
        "ABOUT_TAB_TEST_EXECUTION_INFO_EXPANDED_TEXT": "Test run started",
        "ABOUT_TAB_ENVIRONMENT_BUTTON": "#About > button:nth-child(12)",
        "ABOUT_TAB_ENVIRONMENT_EXPANDED_TEXT": "Plugins",
        "ALL_TESTS_TAB": "body > div > span.tab > div > span:nth-child(2) > button",
        "ALL_TESTS_TAB_FIRST_TEST": "#All\ Tests > button:nth-child(1)",
        "ALL_TESTS_TAB_FIRST_TEST_RESULT": "#All\ Tests > div:nth-child(2) > pre",
        "FAILURES_TAB": "body > div > span.tab > div > span:nth-child(3) > button",
        "FAILURES_TAB_FIRST_TEST": "#Failures > button:nth-child(1)",
        "FAILURES_TAB_FIRST_TEST_RESULT": "#Failures > div:nth-child(2) > pre",
        "PASSES_TAB": "body > div > span.tab > div > span:nth-child(4) > button",
        "PASSES_TAB_FIRST_TEST": "#Passes > button:nth-child(1)",
        "PASSES_TAB_FIRST_TEST_RESULT": "#Passes > div:nth-child(2) > pre",
        "SKIPPED_TAB": "body > div > span.tab > div > span:nth-child(5) > button",
        "SKIPPED_TAB_FIRST_TEST": "#Skipped > button:nth-child(1)",
        "SKIPPED_TAB_FIRST_TEST_RESULT": "#Skipped > div:nth-child(2) > pre",
        "XFAILS_TAB": "body > div > span.tab > div > span:nth-child(6) > button",
        "XFAILS_TAB_FIRST_TEST": "#Xfails > button:nth-child(1)",
        "XFAILS_TAB_FIRST_TEST_RESULT": "#Xfails > div:nth-child(2) > pre",
        "XPASSES_TAB": "body > div > span.tab > div > span:nth-child(7) > button",
        "XPASSES_TAB_FIRST_TEST": "#Xpasses > button:nth-child(1)",
        "XPASSES_TAB_FIRST_TEST_RESULT": "#Xpasses > div:nth-child(2) > pre",
        "RERUNS_TAB": "body > div > span.tab > div > span:nth-child(8) > button",
        "RERUNS_TAB_FIRST_TEST": "#Reruns > button:nth-child(1)",
        "RERUNS_TAB_FIRST_TEST_RESULT": "#Reruns > div:nth-child(2) > pre",
        "FULL_OUTPUT_TAB": "body > div > span.tab > div > span:nth-child(11) > button",
        "FULL_OUTPUT_TAB_EXPANDED_TEXT": "#Full\ Output > pre",
        "FOLDED_OUTPUT_TAB": (
            "body > div > span.tab > div > span:nth-child(12) > button"
        ),
        # "FOLDED_OUTPUT_TAB_SUMMARY_SECTION": (
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
        "FOLD_ACTIONS_TAB_FOLD_UNFOLD_ACTION_TEXT": "Fold/Unfold Action",
        "FOLD_ACTIONS_TAB_SHOW_HIDE_ACTION": "#toggle-details",
        "FOLD_ACTIONS_TAB_SHOW_HIDE_ACTION_TEXT": "Folded",
    }
