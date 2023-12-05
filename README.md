[![Build Status](https://app.travis-ci.com/jsh/trendlist.svg?branch=master)](https://app.travis-ci.com/jsh/trendlist)
[![Documentation Status](https://readthedocs.org/projects/trendlist/badge/?version=latest)](https://trendlist.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jsh/trendlist-notebooks/master)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/jsh/trendlist)

# pytest-tui
## A pytest plugin for viewing test run results, with console scripts to launch a Text User Interface (TUI) or an HTML page

### TUI:
![2022-05-01 19 25 19](https://user-images.githubusercontent.com/4308435/166174159-b442a5b5-416d-42a0-badd-7401e9980e47.gif)

### HTML:
![2022-08-27 08 07 11](https://user-images.githubusercontent.com/4308435/187034046-312b1ee8-0f7b-49a1-994f-9c38a9d3941c.gif)

### Log Folding:
![2023-04-11 23 56 57](https://user-images.githubusercontent.com/4308435/231364763-132e8c35-cb61-4172-9686-176d84c038ca.gif)

## Introduction
When you run Pytest campaigns that produce a lot of terminal output (e.g. with many tests, very detailed output, or with multiple failures), the standard Pytest output can make it difficult to examine the results. You end up scrolling way back in the terminal, looking for that one test you want to examine more closely. Pytest-tui provides a Text User Interface (TUI) and an HTML page that aim to make it easier to find the information you're looking for.

Test results are categorized in the same way Pytest does it:

- By outcome: `[Pass|Fail|Error|Skipped|Xpass|Xfail]`
- By output section: `[Summary|Full|Errors|Passes|Failures|Warnings]`

The intent it to make it easier for you to find the specific results you want so you can examine it without all the other results getting in your way.

How does it work in practice? Easy. You just run your Pytest campaigns like you normally would, adding the command line option `--tui` (`pytest --tui`). Your test session will proceed as it always does (always in verbose mode), showing you the familiar terminal output while running. Then, at the end of the session, a TUI or an HTML page can be launched via the included console scripts (`tui` and/or `tuih`). The results are displayed on-screen or in-browser for you to examine. When you're done, just exit the TUI to go back to the terminal, or close the HTML page. Don't worry about losing your test session data. Results are stored to local disk and you can always relaunch the TUI or HTML page using those same console scripts.

Output sections and individual test results are expandable/collapsible, and test summary statistics are displayed for convenience. Both the TUI and the HTML page retain the original pytest ANSI-encoded color output, lending a familiar look and feel.

## Features
- **New** in 1.10.0 Regex-based folding on the HTML page, configurable by user-provided regex! See "Python Regex Folding" section below.
- **New** in 1.9.1 Log message folding on the HTML page, configurable by log level. See "Python Log Message Folding" section below.
- Launch either or both of the [Textual](https://github.com/Textualize/textual) TUI or the HTML page using built in console scripts
- ANSI text markup support - whatever the output on your console looks like is how things are going to show up in the TUI
- Mouse and keyboard support (including scrolling)
- Support for all output formats/modes:
  - `-v`, `-vv`, `-no-header`, `--showlocals`, `--color=<yes|no|auto>`
  - all variants of `--tb` except "native"
  - "live-log" (aka log_cli)
- Support for other, simple output-manipulating plugins:
  - `pytest-clarity`
  - `pytest-emoji`
  - `pytest-icdiff`
  - `pytest-rerunfailures`
  - etc.
- Not supported: plugins that take over the console in other ways, like
  - `pytest-sugar`
  - `pytest-emoji-output`
  - `pytest-timestamp`
- Untested:
  - `pytest-xdist`
  - `loguru`

## Requirements
- Pytest >= 6.2.5
- Python >= 3.8 (but see "Known Limitations/Issues" below if you want to run 3.10+)

## Installation

For most users, simply issue the command `pip install pytest-tui` and you are good to go.

For those users wishing to install via a requirements.txt file, they are located in the /requirements directory.

## Usage

### Running Your Tests

Pretty much just run pytest like you always do, adding the `--tui` option to the list of command line options:

`pytest --tui <whatever-else-you-normally-do>`

In some environments, where the working directory for pytest has been changed from the default, it may be necessary to cd into the working directory in order to successfully launch the TUI or HTML. Basically, you need to be in the parent directory of wherever the `/tui_files` folder has been placed by the plugin after a test run. This is a known issue and will be fixed at some point.

### Sample / Demo Tests

If you would like some dummy tests that will allow you to take pytest-tui for a testdrive, copy all the files at https://github.com/jeffwright13/pytest-tui/tree/main/demo-tests into a folder called `demo-tests/` where your test environment resides. You will need the additional libraries listed in /requirements/requirements-dev.txt, so install them (`pip install -r requirements-dev.txt`). Then:

`pytest demo-tests/`

### Looking at Results After Quitting TUI

If you have already exited the TUI and would like to re-enter it with the same data generated from the last Pytest run, simply type `tui`. To re-launch the HTML page using your default browser, issue the command `tuih`.

### TUI Copy/Paste

On Linux terminals, you can typically press and hold the SHIFT key on your keyboard to temporarily bypass the TUI and access the terminal's native mouse copy/paste functionality (commonly, click-drag-release or double-click to select text, middle-click to paste). This copy/paste works with the terminal's selection buffer, as opposed to the TUI's buffer.

On Windows, use the ALT key while click-dragging the mouse. Mac users can get the same effect with the Option key.

### Generating and viewing the HTML File

The HTML output file is located at `<cwd>/tui_files/html_report.html`. The HTML file is automatically generated when a test run is completed with the "--tui" option. It can also be generated manually with the `tuih` script by invoking it on the command line.

### Visibility

Sometimes it can be difficult to read the terminal output when rendered on the HTML report. Pytest embeds ANSI color codes in its output, which are interpreted by a terminal program to display various colors for text. Pytest-tui takes these ANSI color codes and translates them to HTML (using the [ansi2html](https://pypi.org/project/ansi2html/) librray). Because the dhe default color scheme for the HTML report is a light background with dark text, it can be difficult to see some of the colors. To address this, there are three buttons that can help. The first ("Toggle Background") allow you to toggle the bakcground color of all console output. This should result in a page that closely resembles the output you would get in a standard terminal environment (assuming you have white text on a black background). The other two buttons, Invert Colors and Remove/Restore Colors, are a bit more drastic in that they affect all text in the report. Experiment and see what works for you. Also note that if you have your browser set to dark mode, or have a theme that changes the default color scheme, this can also affect the visibility of the text.
### "Folding" output in the HTML report

New in 1.11.0 is the integrated "folding" feature, which will automatically roll up any output lines from your test's output which match a regex (or regexes) specified in the file given on the command line. This option allows you to match on specific lines of console output from pytest, and 'fold' them (hide them).

The folding feature is activated by passing the `--tui-regexfile` option (see `pytest --help`), and setting the path of a file containing the desired regex or regexes.

The file itself must contain plain text (UTF-8 encoded) with either a single regex, specified on a single line of the file; or two 'marker' patterns, specified in two consecutive lines of the file. If there is a single line in the file, that line is assumed to contain a regular expressoin that will cause the folding action to be used on any line in the console output of pytest if that line matches the regex. Consecutive lines that match will be folded into the same section. If there are two lines in the regex file, the first line is assumed to be a start marker, and the second line is assumed to be a stop marker. The folding action will be applied to all lines between the start and stop markers

Ideas and tips for folding:
- Run all tests with DEBUG level logging, but only view those DEBUG messages when necessary. I find this option particularly helpful when trying to debug a test that is only failing intermittently.
- Mark certain sections of a test's output with a pair of start/end markers. If you have test output that is very chatty, but you only want to see it when you need to, this is a good option. For example, if you have a test that is making a bunch of API calls, and you want to see the output of those calls, but only when the test fails, you can mark the start and stop of the API calls with a pair of markers, and then fold them away when you don't need to see them.
- Use the non-printable characters 'ZWS' and 'ZWJ' ((Zero Width Space)[https://en.wikipedia.org/wiki/Zero-width_space] / (Zero Width Joiner)[https://en.wikipedia.org/wiki/Zero-width_joiner]) as start and stop markers. The visual impact on the output is minimal (only inserts one visible space), and the regex pattern is very unlikely to match anything else in the output. The repo contains a file called `nonprintable_​​characters.txt` that contains cobinations of these characters, which can be used as a starting point for your own regexes.

## Known Limitations / Issues

- Python support for 3.10+ is not guaranteed. Changes were made to the `importlib.metadata` library that are not backwards-compatible, and may result in exceptions when attempting to run. I have not had the chance to chase this down definitively, so until such a time that I fully understand the issue, I recommend using Python 3.8 or 3.9. Of course, YMMV...give it a try, and let me know how things go. :-)
- User interfaces need work:
  - Overall layouts need optimization (I am definitely not a UX guy)
  - Textual interface may be sluggish, esp. if run within an IDE
  - All code here is like a sausage factory: pleasant enough, until you look inside - do so at your own peril!
- Not fully tested with all combinations of output formats. Probably some use-cases where things won't work 100% right.
- `pytest-tui` is currently incompatible with pytest command line option `--tb=native`, and will cause an INTERNALERROR if the two are used together.
- HTML page cannot offer clickable links to local filesystem. This is one of the workflows I depend on when using iTerm2...traceback lines with a `file://` URL to a locally-hosted resource are clickable, and open up my IDE to that line in that file. Unfortunately, web browsers are much more security-minded than terminal apps, and actions like this are strictly disallowed.

## History

This project was originally envisioned to only show test failures, and allow the user to 'fold' the details of the failed tests by clicking a line so that the details would alternately show/hide. In fact, the original repo was called `pytest-fold`. As development progressed, it became clear that what was really needed was a real TUI, one that organized the output in such a way that all of pytest's output was available in a more streamlined way.

Several TUIs (using different TUI libraries) have been cycled through this project. The Textual interface is the only one currently supported, since some internal optimization has been done to make the results simpler to consume. However, other TUIs should be able to be integrated without too much work (e.g. Asciimatics, PyTermTk, pyermgui, etc.). Same would be true of a GUI. Contact the author if you have a desire to implement one of these. The results of any given testrun are collected and sorted in such a way that it should relatively simple to take them and put them into the presentation mode of choice.

The HTML feature was put into place because of some minor limitations the author found in the available HTML plugins (miscounted totals in some corner cases, no color-coded output, inability to show output from the pytest `live logs` option). There is no intent to replace existing HTML plugins, but if you like this one, please do spread the word. :-)

## Reporting Issues

If you encounter any problems, have feedback or requests, or anything else, please [file an issue](https://github.com/jeffwright13/pytest-tui/issues/new), along with a detailed description.

## Contributing

Contributions are welcome. Please run pyflakes, isort and black on any code before submitting a PR.

I have tried to make the TUIs and the HTML page as clean as possible, but I am not a UI expert and I am sure many improvements could be made. If you are slick with user interfaces, I would love some help!

## License

Distributed under the terms of the MIT license, "pytest-tui" is free and open source software.
