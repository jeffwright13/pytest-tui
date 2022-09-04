# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2022-09-04

- Open up HTML real estate with dropdown containing console output sections (which are presumably lesser-used).
- Make autolaunch False by default for both TUI and HTML.

## [1.3.3] - 2022-09-04

- Fixed error msg re: open file at end of run when pytest is run w/o --tui option.
- Fixed persistent non-wrapping <pre> text in HTML output.

## [1.3.2] - 2022-08-31

- Fixed issue where 'passes_section' was being rendered even if no Passed testcases.

## [1.3.1] - 2022-08-27

- Tweaked colors.
- Cleaned up CSS a bit.

## [1.3.0] - 2022-08-27

- Changed to output HTML as one file, with all included CSS and JS content. This makes it portable when sharing results files.
- Removed unuse "Reruns" section. Reruns are still supported, just not broken out individually. This is more in line with how pytest treats the Reruns section anyway. Reruns are categorized P/F/S/XP/XF just as normal tests are.
- Remove duplicate 'lastline' in About section.
- Implemented dynamic inclusion/removal of section and results tabs, depending on if they have content or not.
- Added 'sticky' CSS styling to top-bar buttons. The top bar now shows up even when scrolling down long pages.
- Fixed a few persistent ANSI issues: no blue markup (was misssing CSS for \x1b94m, 'bright blue'); and non-marked-up section content.

## [1.2.1] - 2022-08-22

- Revamp console-line categorization algorithm to accomodate variations in user environment more easily
- Add support for `live log` sections
- Fix multiple bugs (although several remain)

## [1.2.0] - 2022-08-19

- Working/revamped HTML file output, with more modern look/feel.
- Fixed tui1 (Textual) so that it works with new internal implementation.
- Retiring tui2 (PyTermTk) for now.
- Reordered/removed some menu items in tuiconf to fit new content/choices.
- Changed output files folder to ./ptt_files.

## [1.1.3] - 2022-08-13

- Fixed bug where if config file existed but was empty, an exception would occur on launching HTML file.

## [1.1.2] - 2022-08-10

- Added chronological results section.
- Cleaned up HTML.

## [1.1.1] - 2022-08-08

- Added TUI autolaunch config variable (default False).
- Cleaned up HTML, and added Metadata show/hide button.

## [1.1.0] - 2022-08-07

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
- Fixed --co bug where TUIs were called although no tests had been run.
- Added this changelog.

## [1.0.0] - 2022-08-01

- Refactored individual results classification to use pytest's 'short test summary info' section, instead of TestReport outcome. This ensures that pytest-tui results are always the same as those of pytest itself.
- Implemented basic HTML report.
- Updated folder structure to place .bin and .html output files in /release.
