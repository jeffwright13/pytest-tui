### Foldable (collapsible) HTML using logging class overrides to mark up certain lines ###

Summary:
- See pytest_tui/tui_logger.py for class definitions
- Used in some tests in /demo_tests (e.g. test_tui_logger.py, test_me.py)
- html_gen.py has been augmented to process the inline markup and display it
- To run, simply `pytest --tui demo_tests/test_tui_logger.py`, then `tuih` to view the HTML output (currently written to separate outfile NEW.html)
- Issues:
 - there are issues (e.g. losing <pre> markup within the foldable sections)
 - would like to use invisible chars so noone can see the inline markup when monitoring standard console or output files
 - have to figure out how to deal with pytests's own output handling (stdlog/stdout/stderr)

Test Ideas:
- in iPython, instantiate basic logger and check logging messsages of various levels with varoius log levels configured on logger
- try with pytest and see how things change:
  - deafault behavior
  - -rA
  - live logs
- do same as above with subclassed tui_logger instances
- try with spread code; nested-call code


NOTES 2022-03-19
================
- File pytest_tui/tui_logger.py contains the TuiLogger class, which is a subclass of logging.Logger
- Also included is the TuiLoggers class, aggregating the various TuiLogger classes, along with class methods used to initialize the custom classes in a test:
  -
