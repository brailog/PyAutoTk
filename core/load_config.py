import yaml
from pathlib import Path
from typing import Dict
from config import logger


def load_configuration() -> Dict:
    _dir = Path(__file__).parent
    with open(f'{_dir}/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    logger.debug(config)
    print(config)
    return config
