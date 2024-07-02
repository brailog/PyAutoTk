import pytest
from core.load_config import load_configuration
from pytest import Session
from config import logger
from pytest import Config
from typing import Dict


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: Config) -> None:
    logger.info('Starting the Pytest configure')
    config_var = load_configuration()
    _set_config_variables(config_var)


def _set_config_variables(config_dict : Dict) -> None:
    pytest.email_account_test = config_dict.get('EMAIL_ACCOUNT_TEST')
    pytest.password_account_test = config_dict.get('PASSWORD_ACCOUNT_TEST')


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: 'Session') -> None:
    logger.info('Starting the Pytest session.')
