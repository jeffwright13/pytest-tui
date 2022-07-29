# pytest-tui
## A Pytest plugin that auto-launches a Text User Interface (TUI) for viewing test run results

### Using Textual TUI:
![2022-05-01 19 25 19](https://user-images.githubusercontent.com/4308435/166174159-b442a5b5-416d-42a0-badd-7401e9980e47.gif)

### Using PyTermTk:
![2022-05-01 19 32 28](https://user-images.githubusercontent.com/4308435/166174568-a1e921a8-fa30-4c3a-ab4a-a402bc50fb40.gif)

## Introduction
When you run Pytest campaigns that produce a lot of terminal output (e.g. with many tests, very detailed output, or with multiple failures), the standard Pytest output can make it difficult to examine the results. You end up scrolling way back in the terminal, looking for that one test you want to examine more closely. Pytest-tui provides a Text User Interface (TUI) that aims to make it easier to find the information you're looking for.

Just run your Pytest campaigns like you normally would, adding the command line option `--tui`. Your test session will proceed as it always does, giving you its familiar terminal output while running. Then, at the end of the session, a TUI of your choice is launched and your results are displayed on-screen for you to examine. When you're done, exit the TUI and you are placed back into the terminal where you were before it was launched. Wait, what? You need to look at those results again? Well, you *could* scroll back in the terminal like you've done in the past. Or, you could execute one of the built-in scripts (e.g. "tui1") and you're back in the TUI again. Easy.

Test results are categorized in the same way Pytest does it:

- By outcome:  `[Pass|Fail|Error|Skipped|Xpass|Xfail]`
- By output section: `[Summary|Full|Errors|Passes|Failures|Warnings]`

The intent it to make it easier for you to find the specific results you want so you can examine it without all the other results getting in your way.

## Features
- Choice of two TUIs: [Textual](https://github.com/Textualize/textual) or [PyTermTk](https://pypi.org/project/pyTermTk/)
- Ability to immediately launch TUIs with existing data using console scripts
- ANSI text markup support - whatever the output on your console looks like is how things are going to show up in the TUI
- Mouse and keyboard support (including scrolling)
- Support for all output formats/modes:
  - `-v`, `-vv`, `-no-header`, `--showlocals`, `--color=<yes|no|auto>`
  - all variants of `--tb` except "native"
- Support for other, simple output-manipulating plugins:
  - `pytest-clarity`
  - `pytest-emoji`
  - `pytest-icdiff`
  - etc.
- Not supported: plugins that take over the console in other ways, like
  - `pytest-sugar`
  - `pytest-emoji-output`
- Option to export console output to HTML (`pytest --tuihtml`)

## Requirements
- Pytest >= 6.2.5
- Python >= 3.8

## Installation
`pip install pytest-tui`

## Usage

### Running Tests

Run the following command from the top-level directory of the codebase you want to test:

`pytest --tui`

This will launch the default TUI. You can optionally specify a different TUI by adding a number (1, 2) to the end of the `--tui` option:

`pytest --tui [--tui1|--tui2|--tuin] <other-pytest-options>`

See `pytest --help` for more info.

To quit the Textual TUI, either click the Quit button, or press `Q`. To quit the PyTermTk TUI, click the Quit button in the upper right.

### Demo Tests
 If you would like some dummy tests that will allow you to take pytest-tui for a testdrive, copy all the files at https://github.com/jeffwright13/pytest-tui/tree/main/demo-tests into a folder called `demo-tests/`. Then:

`pytest demo-tests/`

### Looking at Results After Quitting TUI

If you have already exited the TUI and would like to re-enter it with the same data generated from the last Pytest run, simply type:

`tui1` (to launch the Textual TUI)
`tui2` (to launch the PyTermTk TUI)

You can run with the `--tuin` option to bypass auto-launch of the TUI. This allows you to gather results now, and look at them in any of the TUIs later.

### Copy/Paste

On Linux terminals, you can typically press and hold the SHIFT key on your keyboard to temporarily bypass TUI and access the terminal’s native mouse copy/paste functionality (commonly, click-drag-release or double-click to select text, middle-click to paste). This copy/paste works with the terminal’s selection buffer, as opposed to the TUI’s buffer.

On Windows, use the ALT key while click-dragging the mouse. Mac users can get the same effect with the Option key.

## HTML Export
Invoke with option `tuihtml` to produce a HTML file that mirrors the full console output from your test run. Outputfile is named `output_html.html`. This topion can be either called by itself, or in conjuction with the other `tui` options.

`pytest --tuihtml`

## Known Limitations / Issues
- User interfaces need work:
  - Overall layouts need optimization
  - PyTermTk interface may get corrupted if resized
  - Textual interface can be slow, esp. if run within an IDE
  - Textual interface #1 (`tui2`) requires user to toggle All (`A`) to see test outputs if the number of tests is large
- Not fully tested with all combinations of output formats. Probably some use-cases where things won't work 100% right.
- `pytest-tui` is currently incompatible with `--tb=native` and will cause an INTERNALERROR if run together.

## History
This project was originally envisioned to only show test failures, and allow the user to 'fold' the details of the failed tests by clicking a line so that the details would alternately show/hide. As development progressed, it became clear that what was really needed was a real TUI, one that organized the output in such a way that all of Pytest's output was available in a more streamlined way.

## Issues
If you encounter any problems, have feedback or requests, or anything else, please [file an issue](https://github.com/jeffwright13/pytest-tui/issues/new), along with a detailed description.

## Contributing
Contributions are very welcome. Please run pyflakes and black on any code before submitting a PR.

I have tried to make the TUIs as clean as possible, but I am not a UI expert and I am sure many improvements could be made. If you are slick with user interfaces, I would love some help!

## License
Distributed under the terms of the MIT license, "pytest-tui" is free and open source software.
