from logging import INFO, Formatter, Logger, StreamHandler, getLogger
from sys import stdout


def get_logger() -> Logger:
    logger: Logger = getLogger("aigelb-evaluation")
    logger.setLevel(INFO)
    handler: StreamHandler = StreamHandler(stdout)
    formatter: Formatter = Formatter(
        "%(name)s - %(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
