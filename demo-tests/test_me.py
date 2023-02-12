from haggis.logs import add_logging_level

from pytest_tui.utils import (
    TUI_FOLD_CONTENT_BEGIN,
    TUI_FOLD_CONTENT_END,
    TUI_FOLD_TITLE,
)
import logging
logger = logging.getLogger()

def test_me():
    print("Test me!")
    logger.critical("CRITICAL")
    logger.error("ERROR")
    logger.warning("WARNING")
    logger.info("INFO")
    logger.debug("DEBUG")
    assert True


add_logging_level("TUI_FOLD", logging.DEBUG - 5)

def test0_verbose_1():
    logger.tui_fold(TUI_FOLD_TITLE)
    logger.info("===> * Running next test iteration * <===")
    logger.tui_fold(TUI_FOLD_CONTENT_BEGIN)
    logger.info("st Next iteration: setting soc on SiteEss to 50%, current_soc is 50%")
    logger.info("st Sending P & Q signals of -4.84 MW, -4.84 MVAr using CommandRealPowerSignal and CommandReactivePowerSignal")
    logger.info("t Setting soc on SiteEss to 10% - current effectiveSoc is 50%")
    logger.info("commanded_p is below ac_charge_plimit, set to ac_charge_plimit: -4.84 MW")
    logger.info("P is preferred over Q, adjust q_limit")
    logger.info("q_limit calculated to be 0 VAr")
    logger.info("commanded_q is below -q_limit, set to 0 VAr")
    logger.info("PowerDevice.totalReactivePowerSetPoint is 0 VAr; expected 0 VAr")
    logger.info("PowerDevice.totalRealPowerSetPoint is -4.84 MW; expected -9.68 MW")
    logger.info("PowerDevice.totalRealPowerSetPoint is -4.84 MW; expected -9.68 MW")
    logger.info("PowerDevice.totalRealPowerSetPoint is -4.84 MW; expected -9.68 MW")
    logger.info("PowerDevice.totalRealPowerSetPoint is -4.84 MW; expected -9.68 MW")
    logger.info("PowerDevice.totalRealPowerSetPoint is -4.84 MW; expected -9.68 MW")
    logger.info("PowerDevice.totalRealPowerSetPoint is -4.84 MW; expected -9.68 MW")
    logger.info("PowerDevice.totalRealPowerSetPoint is -9.68 MW; expected -9.68 MW")
    logger.info("Verifying site responds with expected power, using input params:")
    logger.info(" Site rated real power: 4.84 MW")
    logger.info(" Site rated reactive power: 4.84 MVAr")
    logger.info(" Site ac discharge real power limit: 4.84 MW")
    logger.info(" Site ac charge real power limit: 4.84 MW")
    logger.info(" Commanded real power: -9.68 MW")
    logger.info(" Commanded reactive power: 0 VAr")
    logger.info("Commanded Real Power was at or below site's acChargePowerLimit of -4.84 MW, so expecting -4.84 MW")
    logger.info("Commanded Reactive Power was within Site limits, so expecting Q of 0 VAr")
    logger.info("Verified site real power -4.84 MW is within 5% of expected real power -4.84 MW")
    logger.info("Verified site reactive power 0 VAr is within 5% of expected reactive power 0 VAr")
    logger.info("True")
    logger.tui_fold(TUI_FOLD_CONTENT_END)
