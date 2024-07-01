import pytest
from core.load_config import load_configuration
from pytest import Session
from config import logger


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: 'Session') -> None:
    logger.info('Starting the Pytest session.')
    load_configuration()
