import logging
from pathlib import Path


class LogLevel:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def ensure_path(path: Path) -> Path:
    """
    Ensure that the directory for the given path exists.
    If it does not exist, create it.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_logger(name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
