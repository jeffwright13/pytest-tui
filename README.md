# pytest-tui
## A Pytest plugin to make console output more manageable

### Using PyTermTk:
![output2](https://user-images.githubusercontent.com/4308435/162344632-552f1284-51a4-46c4-b389-0352636f65bb.gif)


### ...using Textual TUI:
![ezgif com-gif-maker](https://user-images.githubusercontent.com/4308435/154848960-391fd62f-4859-4d2b-8d03-9f55f4b04cad.gif)

## Introduction
Do you run long Pytest campaigns and get lots of failures? And then spend the next 10 minutes scrolling back in your console to find the one traceback that you're interested in drilling down into? Well, maybe `pytest-tui` can help. `pytest-tui` is a plugin that captures the output from your Pytest test runs, then automatically launches an interactive Text User Interface (TUI) where all your test results are categorized by (a) outcome [Pass|Fail|Error|Skipped|Xpass|Xfail], and (b) output section [Summary|Full|Errors|Passes|Failures|Warnings]. The intent it to make it easier for you to find the specific result you want so you can examine it without all the other results to get in your way.

## Features
- Choice of two TUIs: Textual and PyTermTk
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

## Requirements
- Pytest >= 6.2.5
- Python >= 3.8

## Installation
`pip install pytest-tui`

## Usage

From top-level directory:

* `pytest --tui`

Or, if you want to get technical about it:

* `pytest --tui [--tui-tui textual1|textual2|pytermtk|none] <other-pytest-options>`

See 'pytest --help' for more info.

To quit the Textual TUI, either click the Quit button, or press `Q`. To quit the PyTermTk TUI, click the Quit button in the upper right.

If you have already exited the TUI and would like to re-enter it with the same data generated from the last Pytest run, simply type:

* `termtxt` (to launch Textual)
* `termtk` (to launch PyTermTk)

You can also run with the `--tui` option enabled but bypass auto-launch of the TUI with the `--ft=n` option.

## Known Limitations / Issues
- Rudimentary user interfaces that need a lot of love:
  - Textual interface can be slow, esp. if run within an IDE
  - PyTermTk interface sometimes gets corrupted if resized
- Not fully tested with all combinations of output formats. Probably some use-cases where things won't work 100% right.
- `pytest-tui` is currently incompatible with `--tb=native` and will cause an INTERNALERROR if run together. (TODO: Fix this.)

## Contributing
Contributions are very welcome. If you are slick with user interfaces, I would love some help there.
Please run pyflakes and black on any code before submitting a PR.

## License
Distributed under the terms of the `MIT`_ license, "pytest-tui" is free and open source software.

## Issues
If you encounter any problems, have feedback or requests, or anything else, please [file an issue](https://github.com/jeffwright13/pytest-tui/issues/new), along with a detailed description.
