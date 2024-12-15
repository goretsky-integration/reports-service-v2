import logging.config
import pathlib
import json
from typing import Final

__all__ = (
    "create_logger",
    "load_logging_config",
    "setup_logging",
    "LOGGING_CONFIG_PATH",
)


LOGGING_CONFIG_PATH: Final[pathlib.Path] = (
    pathlib.Path(__file__).parent.parent / "logging_config.json"
)


def create_logger(name: str) -> logging.Logger:
    """
    Create logger which does not propagate event to root logger.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    return logger


def load_logging_config(
    file_path: pathlib.Path = LOGGING_CONFIG_PATH,
) -> dict:
    config_json = file_path.read_text(encoding="utf-8")
    return json.loads(config_json)


def setup_logging(
    file_path: pathlib.Path = LOGGING_CONFIG_PATH,
) -> None:
    logging_config = load_logging_config()
    logging.config.dictConfig(logging_config)
