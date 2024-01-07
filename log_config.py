import logging
import logging.config
from datetime import datetime, timezone


class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        t = dt.strftime("%Y-%m-%d %H:%M:%S")
        return f"{t} UTC"


logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "utc": {
            "format": " %(asctime)s %(levelname)-8s %(name)-12s %(message)s",
            "()": UTCFormatter,  # special nomenclature to use custom formatter
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "utc",  # Use the UTCFormatter here
            "stream": "ext://sys.stderr",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {},
}

# Explicitly set the formatter for the root logger
logging.getLogger().handlers[0].setFormatter(logging_config["formatters"]["utc"])

for logger_name, logger_config in logging_config["loggers"].items():
    logger_config["handlers"] = ["console"]
    logger_config["propagate"] = False  # Avoid double logging

logging.config.dictConfig(logging_config)
