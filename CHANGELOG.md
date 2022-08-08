# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2022-08-08

- Refactored HTML code to fix several small but annoying issues.
- Added new configuration console script `tuiconf` that allows user to change/store settings for:
  - TUI choice (`tui1` (Textual) or `tui2` (PyTermTk))
  - HTML "light" or "dark" page coloring scheme
  - HTML autolaunch (y or n)
  - Custom coloring capability for HTML scheme
- Removed old `tui1` and `tui2` console scripts, replacing with a single `tui` version that launches the configured TUI as set using `tuiconf`
- Added new console script `tuih`, which creates and optionally launches the HTML output from the last testrun session.
- Changed name of output file folder to /pytest_tui_files. This is where the .bin and .html files now reside.
- Fixed issue where if no tests were run and either TUI was launched, they would crash.
- Replaced previous dummy environment button data with actual environment data from pytests's output.

## [1.0.1] - 2022-08-02

- Implemented threading in final testing stage so that HTML and TUI can be launched at the same time.
- Adede this changelog.

## [1.0.0] - 2022-08-01

- Refactored individual results classification to use pytest's 'short test summary info' section, instead of TestReport outcome. This ensures that pytest-tui results are always the same as those of pytest itself.
- Implemented basic HTML report.
- Updated folder structure to place .bin and .html output files in /release.
