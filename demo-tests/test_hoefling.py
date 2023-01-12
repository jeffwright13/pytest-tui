import logging

import pytest

logger = logging.getLogger()


LOREM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec rutrum molestie arcu, id consectetur nisl commodo luctus. Curabitur ac eros efficitur, bibendum nibh volutpat, lobortis arcu. Nam gravida condimentum felis eu porttitor. Fusce at mi et purus condimentum facilisis et nec felis. Vivamus aliquet, elit eu sagittis bibendum, elit velit scelerisque tellus, et ornare lectus nulla eget diam. Mauris eleifend lectus vel ipsum vehicula malesuada. Ut vitae arcu ac elit bibendum elementum. Aliquam quis sagittis justo. Maecenas sit amet sodales velit.

Curabitur vel felis finibus, auctor ligula ut, tempus leo. Aenean turpis lectus, aliquet non euismod a, sagittis non nisl. Nulla pretium ultricies augue ut egestas. Mauris vel ex nec lorem rutrum varius. Phasellus laoreet elit eu volutpat accumsan. Morbi justo ligula, accumsan sed efficitur sit amet, ornare vel massa. Proin a tempor risus, at imperdiet augue. Cras sed felis sagittis, pellentesque dui vel, luctus nunc. Sed sed elementum nibh.

Sedsodalesauctorlaoreet.Pellentesqueinaccumsanleo, idultriciesarcu. Inegestas,arcuidtristiquepulvinar, nullasapienpharetraerat, amollisrisustortoractellus. Quisquetemporodioquislacusmaximus, vitaeconguejustomattis. Nuncsollicitudinaloremetvestibulum.Etiamquispretiumvelit. Nullavelduisitametnunclobortisviverra. Proinconsequat, purusetlaoreetfeugiat, risusvelitsagittismassa, acimperdietlectusdiamsitametodio. Vestibulumalaciniaquam.
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
