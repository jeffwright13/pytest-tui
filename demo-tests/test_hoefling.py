import pytest
import logging


logger = logging.getLogger()


LOREM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec rutrum molestie arcu, id consectetur nisl commodo luctus. Curabitur ac eros efficitur, bibendum nibh volutpat, lobortis arcu. Nam gravida condimentum felis eu porttitor. Fusce at mi et purus condimentum facilisis et nec felis. Vivamus aliquet, elit eu sagittis bibendum, elit velit scelerisque tellus, et ornare lectus nulla eget diam. Mauris eleifend lectus vel ipsum vehicula malesuada. Ut vitae arcu ac elit bibendum elementum. Aliquam quis sagittis justo. Maecenas sit amet sodales velit.

Curabitur vel felis finibus, auctor ligula ut, tempus leo. Aenean turpis lectus, aliquet non euismod a, sagittis non nisl. Nulla pretium ultricies augue ut egestas. Mauris vel ex nec lorem rutrum varius. Phasellus laoreet elit eu volutpat accumsan. Morbi justo ligula, accumsan sed efficitur sit amet, ornare vel massa. Proin a tempor risus, at imperdiet augue. Cras sed felis sagittis, pellentesque dui vel, luctus nunc. Sed sed elementum nibh.

Sed sodales auctor laoreet. Pellentesque in accumsan leo, id ultricies arcu. In egestas, arcu id tristique pulvinar, nulla sapien pharetra erat, a mollis risus tortor ac tellus. Quisque tempor odio quis lacus maximus, vitae congue justo mattis. Nunc sollicitudin a lorem et vestibulum. Etiam quis pretium velit. Nulla vel dui sit amet nunc lobortis viverra. Proin consequat, purus et laoreet feugiat, risus velit sagittis massa, ac imperdiet lectus diam sit amet odio. Vestibulum a lacinia quam.

Ut ut metus nisl. Praesent eu gravida dolor. Vestibulum quis congue dui. Cras in bibendum massa, quis aliquet eros. Aenean sollicitudin vehicula lacinia. Pellentesque volutpat augue magna, a posuere orci aliquet quis. Maecenas convallis velit et velit cursus sollicitudin. Nunc quis faucibus purus, eu laoreet velit. Sed nibh metus, efficitur at aliquet a, lacinia eget ex. Suspendisse potenti. Integer et tortor vitae augue consequat tempus at sed nisl. Vivamus at nisl ut nulla sagittis sollicitudin eget nec ante. Aliquam cursus ut risus a finibus.

Donec eu odio ac nisl fringilla bibendum. Maecenas luctus posuere velit, sit amet consequat nulla dictum nec. Proin ultrices est at mauris luctus, non accumsan turpis egestas. Ut porttitor, odio ac eleifend bibendum, quam justo imperdiet magna, vel scelerisque tortor ligula id nulla. Fusce in orci rutrum, ultrices lacus non, suscipit erat. Vestibulum ut mauris semper, laoreet eros vitae, faucibus tortor. Sed non est sed nunc ultricies malesuada.
"""


def test_1():
    logger.critical(LOREM)
    logger.error(LOREM)
    logger.warning(LOREM)
    logger.info(LOREM)
    logger.debug(LOREM)
    assert False


def test_2():
    logger.critical(LOREM)
    logger.error(LOREM)
    logger.warning(LOREM)
    logger.info(LOREM)
    logger.debug(LOREM)
    raise RuntimeError("call error")


@pytest.fixture
def f():
    logger.critical(LOREM)
    logger.error(LOREM)
    logger.warning(LOREM)
    logger.info(LOREM)
    logger.debug(LOREM)
    raise RuntimeError("setup error")


def test_3(f):
    logger.critical(LOREM)
    logger.error(LOREM)
    logger.warning(LOREM)
    logger.info(LOREM)
    logger.debug(LOREM)
    assert True
