from io import StringIO
from typing import ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

import pytest
import os

from helpers import case_names
from src.utils.logger import logger, configure_logger

LoggerTestCase = NamedTuple(
    "log_test",
    [("log_path", str),
     ("log_level", str),
     ("log_format", str),
     ("result", str),
     ("expectation", ContextManager),
     ("name", str)],
)

LoggerTestCases = [
    LoggerTestCase(log_path='logs/testing.log',
                   log_level="INFO",
                   log_format='{message}',
                   result=None,
                   expectation=does_not_raise(),
                   name="succesfull_save"),
]


@patch("sys.stdout", new_callable=StringIO)
@pytest.mark.parametrize(
    "need_mp, level, format, expected",
    (
        (False, "DEBUG", "{message}", "-hi-\n"),
        (False, "INFO", "{message}", "-hi-\n"),
        (True, "DEBUG", "{message}", "-hi-\n"),
    ),
)
def test_create_logger(mock_stdout, monkeypatch, mocker, need_mp, level, format, expected):
    mock_conf = mocker.MagicMock()
    mock_conf.log_file = 'logs/testing.log'
    mocker.patch('src.utils.logger.Config', return_value=mock_conf)
    
    if need_mp:
        monkeypatch.setenv("LOG_LEVEL", level)
        configure_logger(
            log_path="", log_level=level, log_format=format)
    else:
        configure_logger(
            log_path="", log_level=level, log_format=format)
    logger.info("-hi-")

    res = mock_stdout.getvalue()
    assert res == expected


@pytest.mark.parametrize("case", LoggerTestCases, ids=case_names(LoggerTestCases))
def test_configure_logger(mocker, case: LoggerTestCase):
    with case.expectation:
        mocker.patch('src.utils.logger.Config.log_file', new=None)
        configure_logger(None, case.log_level, case.log_format)
        assert len(logger._core.handlers) == 1
    
        mocker.patch('src.utils.logger.Config.log_file', new='logs/testing.log')
        configure_logger(None, case.log_level, case.log_format)
        assert len(logger._core.handlers) == 2
        assert os.path.isfile(case.log_path) == True


def test_log_before_disable(writer):
    logger.add(writer, format='{message}')
    logger.enable("")
    logger.debug("yes")

    logger.disable("")
    logger.debug("no")

    result = writer.read()
    assert result == "yes\n"
