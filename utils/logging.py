import logging
import logging.config
import json

from utils import projpath

def setup_console_output(min_level="INFO"):
    config_fpath = projpath("resources/logging_config.json")
    with open(config_fpath) as json_file:
        config = json.load(json_file)
        config["handlers"]["console"]["level"] = min_level
        config["root"]["level"] = min_level

    logging.config.dictConfig(config)
    logging.info("Logging Config was loaded.")


class _ColoredFormatter(logging.Formatter):
    """
    This Formatter will simply color some of the log output using Escape Sequences.
    """

    def __init__(self, fmt=None, datefmt=None, style='%'):
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        if record.levelno >= logging.ERROR:
            s = "\033[31m" + s + "\033[00m"
        elif record.levelno == logging.WARNING:
            s = "\033[33m" + s + "\033[00m"
        return s