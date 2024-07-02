import os
import time
from pathlib import Path
import pytest
import traceback
import pandas as pd
from core.load_config import load_configuration
from pytest import Session
from config.logger import setup_logger
from config import logger
from pytest import Config
from typing import Dict, AnyStr
from pytest import Item
from pytest import TestReport

ROOT_DIR = Path(__file__).parent
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
TEST_RESULTS = list()

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: Config) -> None:
    config_var = load_configuration()
    _set_config_variables(config_var)
    current_timestamp = str(time.time())
    pytest.session_folder = _create_folder(LOGS_DIR, current_timestamp)
    setup_logger(pytest.session_folder)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    pass


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report: TestReport) -> None:
    if report.when == 'call':
        result = 'passed' if report.passed else 'failed'
        error_line = report.location[0] if report.failed else None
        duration = report.duration
        nodeid_parts = report.nodeid.split("::")
        file_path = nodeid_parts[0]
        project = file_path.split(os.sep)[1]
        suite = file_path.split(os.sep)[2]
        test_case_name = os.path.basename(file_path).replace('.py', '')

        TEST_RESULTS.append({
            'test_case': test_case_name,
            'result': result,
            'error_line': error_line,
            'duration': duration,
            'project': project,
            'suite': suite,
        })

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    df = pd.DataFrame(TEST_RESULTS)
    if hasattr(pytest, 'session_folder'):
        dir_csv_path = pytest.session_folder
        df.to_csv(f'{dir_csv_path}/summary_db_result.csv', index=False)

    print(df)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: Item) -> None:
    logger.info(f"======= TEST CASE: {item.name} STARTED =======")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item: Item, nextitem: Item) -> None:
    nextitem_name = nextitem.name if hasattr(nextitem, "name") else ""
    logger.info(f"======= TEST CASE: {item.name} FINISHED. NEXT WILL BE: {nextitem_name} =======")

@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    logger.error(f"Exception occurred at {call.excinfo.traceback[-1].path}:{call.excinfo.traceback[-1].lineno}")
    logger.error(f"Exception type: {call.excinfo.typename}")
    logger.error(f"Exception value: {call.excinfo.value}")
    formatted_tb = ''.join(traceback.format_tb(call.excinfo.tb))
    short_tb = formatted_tb.split('\n')[-5:]
    logger.error(f"Short traceback:\n{''.join(short_tb)}")


def _create_folder(path: str, folder_name: str) -> AnyStr:
    if not os.path.exists(path):
        os.mkdir(path)

    new_folder = os.path.join(path, folder_name)
    is_dir_created = os.path.exists(new_folder)
    if is_dir_created:
        return ""
    os.mkdir(os.path.join(new_folder))
    return new_folder


def _set_config_variables(config_dict: Dict) -> None:
    pytest.email_account_test = config_dict.get('EMAIL_ACCOUNT_TEST')
    pytest.password_account_test = config_dict.get('PASSWORD_ACCOUNT_TEST')
