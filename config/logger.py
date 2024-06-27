import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler_info = logging.FileHandler('info_hextec_logger.log')
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.setFormatter(formatter)

    file_handler_debug = logging.FileHandler('debug_hextec_logger.log')
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_debug.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler_info)
    logger.addHandler(file_handler_debug)
    logger.addHandler(console_handler)

    logger.info("INFO Logger is set up.")
    logger.warning("WARNING is set up.")
    logger.debug("DEBUG is set up.")
