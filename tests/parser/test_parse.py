from typing import ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise

import pytest
import os

from helpers import case_names
from src.parser.parser import Parser
from src.reader.docx_reader import DOCXReader
from _fixtures import new_doc_parser


ParseFileTestCase = NamedTuple(
    "parse_test",
    [("input_dir", str),
     ("file", str),
     ("output_dir", str),
     ("result", str),
     ("expectation", ContextManager),
     ("name", str)],
)

ParseFileTestCases = [
    ParseFileTestCase(input_dir='tests/test_data/documents_tests/',
                      file="Васильев Дмитрий Андреевич.docx",
                      output_dir="tests/test_data/test_output/",
                      result=None,
                      expectation=does_not_raise(),
                      name="succesfull_save"),
]


@pytest.mark.parametrize("case", ParseFileTestCases, ids=case_names(ParseFileTestCases))
def test_parse_file(new_doc_parser: Parser, case: ParseFileTestCase):
    with case.expectation:
        reader = DOCXReader()
        files = reader.read_dir(case.input_dir)
        new_doc_parser.parse(files, case.output_dir)
        saved_file = os.path.join(
            case.output_dir, 'Васильев Дмитрий Андреевич.md')
        assert os.path.isfile(saved_file) == True
