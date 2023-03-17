from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, getLogger

import pytest

from pytest_tui.tui_logger import (
    ContentBeginLogger,
    ContentEndLogger,
    ContentLogger,
    TitleLogger,
)


@pytest.fixture
def tui_loggers():
    logger = getLogger("StandardPythonLogger")
    title_logger = TitleLogger("TitleLogger")
    content_begin_logger = ContentBeginLogger("ContentBeginLogger")
    content_logger = ContentLogger("ContentLogger")
    content_end_logger = ContentEndLogger("ContentEndLogger")
    logger.setLevel(DEBUG)
    title_logger.setLevel(DEBUG)
    content_begin_logger.setLevel(DEBUG)
    content_end_logger.setLevel(DEBUG)

    return (
        logger,
        title_logger,
        content_begin_logger,
        content_logger,
        content_end_logger,
    )
