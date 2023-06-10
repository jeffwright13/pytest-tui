# import pytest

# @pytest.mark.test_tui_with_pytester
# def test_plugin_options(pytester):
#     """Test the plugin options."""
#     # Run pytest without any options
#     result = pytester.runpytest()

#     # Assert that the plugin options are not set
#     assert result.ret == 0
#     assert result.parseopt("_tui") is None
#     assert result.parseopt("_tui_htmlfile") is None
#     assert result.parseopt("_tui_regexfile") is None

#     # Run pytest with the --tui option
#     result = pytester.runpytest("--tui")

#     # Assert that the --tui option is set
#     assert result.ret == 0
#     assert result.parseopt("_tui").value == True
#     assert result.parseopt("_tui_htmlfile") is None
#     assert result.parseopt("_tui_regexfile") is None

#     # Run pytest with the --tui-html option and a custom file path
#     html_file = "custom_html_report.html"
#     result = pytester.runpytest(f"--tui-html={html_file}")

#     # Assert that the --tui-html option is set with the correct file path
#     assert result.ret == 0
#     assert result.parseopt("_tui").value == True
#     assert result.parseopt("_tui_htmlfile").value == html_file
#     assert result.parseopt("_tui_regexfile") is None

#     # Run pytest with the --tui-regexfile option and a custom file path
#     regex_file = "custom_regex.txt"
#     result = pytester.runpytest(f"--tui-regexfile={regex_file}")

#     # Assert that the --tui-regexfile option is set with the correct file path
#     assert result.ret == 0
#     assert result.parseopt("_tui").value == True
#     assert result.parseopt("_tui_htmlfile") is None
#     assert result.parseopt("_tui_regexfile").value == regex_file
