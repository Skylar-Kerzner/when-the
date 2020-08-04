import logging
import sys

from loguru import logger

from . import config as cfg

logging.getLogger().handlers = []

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "level": cfg.logging_level,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name} [{process.id}]</cyan> | <level>{message}</level>"
        }
    ]
)