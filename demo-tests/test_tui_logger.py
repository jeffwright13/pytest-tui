import random
from logging import getLogger, DEBUG, WARNING, ERROR, INFO

from pytest_tui.utils import TUI_FOLD_TITLE_BEGIN, TUI_FOLD_TITLE_END, TUI_FOLD_CONTENT_BEGIN, TUI_FOLD_CONTENT_END
from rich import inspect
from pytest_tui.tui_logger import TitleLogger, ContentLogger, ContentBeginLogger, ContentEndLogger

logger = getLogger("StandardPythonLogger")
title_logger = TitleLogger("TitleLogger")
content_begin_logger = ContentBeginLogger("ContentBeginLogger")
content_logger = ContentLogger("ContentLogger")
content_end_logger = ContentEndLogger("ContentEndLogger")
logger.setLevel(INFO)
title_logger.setLevel(INFO)
content_begin_logger.setLevel(INFO)
content_end_logger.setLevel(INFO)

def pass_or_fail():
    return random.choice([True, False, False])

def lorem_pass() -> str:
    return """PASS Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?

    At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."""

def lorem_fail() -> str:
    return """FAIL Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?

    At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."""

def test_nested_outer_function():
    logger.info("This is just a regular log message at the beginning of the nested outer function.")
    title_logger.warning("Click into me to see All The Logs!")
    content_begin_logger.warning("Initial log entry from nested_outer_function")
    content_logger.warning("Second log entry from nested_outer_function")
    logger.info("This is just a regular log message in the middle of the nested outer function.")

    nested_inner_function()

    assert True
    content_end_logger.warning("Final log entry from nested_outer_function")
    logger.warning("This is just a regular log message at the end of the nested outer function.")

def nested_inner_function():
    logger.info("This is just a regular log message at the beginning of the nested inner function.")
    title_logger.warning("Click into me to see The Inner Logs!")
    content_begin_logger.warning("Initial log entry from nested_inner_function")
    content_logger.warning("Second log entry from nested_inner_function")
    logger.warning("This is just a regular log message in the middle of the nested inner function.")
    assert True
    content_end_logger.warning("Final log entry from nested_inner_function")
    logger.info("This is just a regular log message at the end of the nested inner function.")

def test_tui_logger_pass():
    title_logger.warning("Big-Ass-Lorem-Pass")
    content_logger.warning(f'{lorem_pass()}')
    assert True

def test_tui_logger_fail():
    title_logger.warning("Big-Ass-Lorem-Fail")
    content_logger.warning(f'{lorem_fail()}')
    assert False

# def test_nested_function_calls(tui_loggers):
#     nested_outer_function()
#     nested_inner_function()
