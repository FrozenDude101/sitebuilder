from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass

import logging
from sys import stdout, stderr


_LOG_LEVEL = logging.getLevelName(logging.INFO)

_FORMATTER = logging.Formatter(
    fmt="%(asctime)s: %(name)s: %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

_STD_HANDLER = logging.StreamHandler(stdout)
_STD_HANDLER.addFilter(lambda l: l.levelno <= logging.WARNING)
_STD_HANDLER.setFormatter(_FORMATTER)

_ERROR_HANDLER = logging.StreamHandler(stderr)
_ERROR_HANDLER.addFilter(lambda l: l.levelno > logging.WARNING)
_ERROR_HANDLER.setFormatter(_FORMATTER)

logger = logging.getLogger()
logger.setLevel(_LOG_LEVEL)
logger.addHandler(_STD_HANDLER)
logger.addHandler(_ERROR_HANDLER)