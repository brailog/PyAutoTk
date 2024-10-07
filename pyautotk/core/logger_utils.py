import logging
import sys
from typing import Optional
from pyautotk.core.config_loader import config


def initialize_logger(
    logger_name: str = "PyAutoTk",
    log_level: str = None,
    log_to_file: Optional[str] = None,
) -> logging.Logger:
    """
    Initializes and configures the logger

    Args:
        logger_name (str): The name to use for the logger. Helps in identifying logs from different components.
        log_level (str): The minimum log level to capture. Default is "INFO".
        log_to_file (Optional[str]): If provided, logs will be written to the specified file path. Default is None.

    Returns:
        logging.Logger: Configured logger instance with the specified name.
    """
    log_level = log_level or config.log_level

    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, log_level.upper(), "INFO"))

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper(), "INFO"))

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        if log_to_file:
            file_handler = logging.FileHandler(log_to_file)
            file_handler.setLevel(getattr(logging, log_level.upper(), "INFO"))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
