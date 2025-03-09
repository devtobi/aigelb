from logging import INFO, Formatter, StreamHandler, getLogger
from sys import stdout


def get_logger():
    logger = getLogger("aigelb-evaluation")
    logger.setLevel(INFO)
    handler = StreamHandler(stdout)
    formatter = Formatter(
        "%(name)s - %(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
