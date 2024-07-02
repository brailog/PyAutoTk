from .logger import setup_logger

def get_logger():
    import logging
    return logging.getLogger('hextec')

logger = get_logger()