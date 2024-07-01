import logging
DEBUG = True


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler_info = logging.FileHandler('info_hextec_logger.log')
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler_info)
    logger.addHandler(console_handler)

    if DEBUG:
        file_handler_debug = logging.FileHandler('debug_hextec_logger.log')
        file_handler_debug.setLevel(logging.DEBUG)
        file_handler_debug.setFormatter(formatter)
        logger.addHandler(file_handler_debug)

    return logger
