from logging import INFO, Formatter, Logger, StreamHandler, getLogger
from sys import stdout
from typing import Iterable, TypeVar


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

T = TypeVar('T')

def log_list(lst: Iterable[T], logger: Logger, msg: str = "") -> None:
    if msg:
        logger.info(msg)
    for element in lst:
        logger.info(f"| {element}")
