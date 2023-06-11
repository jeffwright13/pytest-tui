# Plugin Test Ideas
## Command-line options verification
- invoke `pytest --help` and verify that the plugin is listed
- invoke `pytest --tui --help` and verify that the plugin is listed
- invoke `pytest --co` and verify a collected list of tests is displayed
- invoke `pytest --co --tui` and verify a collected list of tests is displayed
- invoke `pytest --tui-html` and verify error msg (requires `--tui`)
- invoke `pytest --tui-regexfile` and verify error msg (requires `--tui`)
- invoke `pytest --tui` and verify:
 - default console output is displayed

## ini options verification
- --ignore flag ignores tests in certain dirs
- test with live logging `log_cli`

## Execution of tests
- invoke `pytest` and verify that the plugin is not invoked
