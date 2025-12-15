from typing import ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise

import pytest
import os

from helpers import case_names
from src.parser.parser import Parser
from _fixtures import new_doc_parser


SaveToMdTestCase = NamedTuple(
    "save_to_md_test",
    [("to_save", dict),
     ("save_path", str),
     ("result", str),
     ("expectation", ContextManager),
     ("name", str)],
)

SaveToMdTestCases = [
    SaveToMdTestCase(to_save={'A': 'a',
                              'B': 'b',
                              'C': 'c'},
                     save_path="tests/test_data/test_output/save_to_md_test_1.md",
                     result=None,
                     expectation=does_not_raise(),
                     name="succesfull_save"),
]


@pytest.mark.parametrize("case", SaveToMdTestCases, ids=case_names(SaveToMdTestCases))
def test_set_templates(new_doc_parser: Parser, case: SaveToMdTestCase):
    with case.expectation:
        new_doc_parser.save_to_md(case.to_save, case.save_path)
        assert os.path.isfile(case.save_path) == True
