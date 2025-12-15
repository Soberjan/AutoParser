from typing import ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise

import pytest
import os
import time

from helpers import case_names
from src.parser.doc_parser import doc_parser
from src.utils.decorators import timer
from src.utils.logger import logger

TimerTestCase = NamedTuple(
    "save_to_md_test",
    [("time", str),
     ("result", str),
     ("expectation", ContextManager),
     ("name", str)],
)

TimerTestCases = [
    TimerTestCase(time=1,
                  result=None,
                  expectation=does_not_raise(),
                  name="succesfull_save"),
]


@timer
def tr(t: float):
    time.sleep(t)
    return True


@pytest.mark.parametrize("case", TimerTestCases, ids=case_names(TimerTestCases))
def test_parse_file(case: TimerTestCase):
    with case.expectation:
        assert tr(case.time) == True
