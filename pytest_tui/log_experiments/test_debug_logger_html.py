# import logging

# logger = logging.getLogger(__name__)

# from pytest_tui.debug_html_logger import DebugLogger, DebugLoggers, DebugLogHandler

# # debug_loggers = DebugLoggers()
# # debug_loggers.localize(name=__name__)
# # debug_logger = debug_loggers.get_debug_loggers()

# debug_logger = DebugLoggers().get_debug_logger()
# print()


# def lorem() -> str:
#     return """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

#     Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci."""


# def calculate(a, b, c) -> float:
#     """Calculate the three-phase power factor of a, b and c"""
#     return (a**3 / 100 + b**3 / 100 + c**3 / 100) ** 0.5


# def test_debug_logger_html():
#     """Test debug logger with HTML report."""
#     logger.warning("Hello, world!")
#     logger.warning(lorem())
#     debug_logger.title()
#     debug_logger.content(lorem())
#     debug_logger.content(calculate(1, 2, 3))
#     debug_logger.content(lorem(), end=True)
#     assert True
