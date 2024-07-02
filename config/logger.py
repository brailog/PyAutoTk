from pathlib import Path
import logging
DEBUG = True


def setup_logger():
    root_dir = Path(__file__).parent.parent

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler_info = logging.FileHandler(f'{root_dir}/logs/info_hextec_logger.log')
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler_info)
    logger.addHandler(console_handler)

    if DEBUG:
        file_handler_debug = logging.FileHandler(f'{root_dir}/logs/debug_hextec_logger.log')
        file_handler_debug.setLevel(logging.DEBUG)
        file_handler_debug.setFormatter(formatter)
        logger.addHandler(file_handler_debug)

    return logger
