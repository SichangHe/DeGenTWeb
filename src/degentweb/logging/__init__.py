"""Custom logging facility that respect module-level log level."""

import logging
import os

logging_levels: list[tuple[str, int]] | None = None


LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(name)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


def _get_or_init_logging_levels():
    global logging_levels
    if logging_levels is not None:
        return logging_levels
    env_log_levels = os.environ.get("LOG_LEVEL", "info").lower()
    logging_levels = []
    for part in env_log_levels.split(","):
        if part == "":
            pass
        elif "=" in part:
            splits = part.split("=")
            assert len(splits) == 2, ("Invalid log level format", part)
            logging_levels.append((splits[0], LEVEL_MAP[splits[1]]))
        else:
            logging_levels.append(("", LEVEL_MAP[part]))
    return logging_levels


def init_logger_w_env_level(module_name: str):
    """Initialize logger with level from environment variable.
    Pass in `__name__` as `module_name`."""
    logging_levels = _get_or_init_logging_levels()
    logging_level = logging.INFO
    for prefix, level in logging_levels:
        if module_name.startswith(prefix):
            logging_level = level
    logger = logging.getLogger(module_name)
    logger.setLevel(logging_level)
    return logger
