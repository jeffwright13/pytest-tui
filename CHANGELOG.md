# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-

## [1.1.0] - 2022-08-02

- Implement threading in final testing stage so that HTML and TUI can be launched at the same time.
- Fix --co bug where TUIs were called although no tests had been run.
- Add this changelog.

## [1.0.0] - 2022-08-01

- Refactor individual results classification to use pytest's 'short test summary info' section, instead of TestReport outcome. This ensures that pytest-tui results are always the same as those of pytest itself.
- Implement basic HTML report.
- Update folder structure to place .bin and .html output files in /release.
