from typing import ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise

import pytest

from helpers import case_names

from src.parser.parser import Parser
from _fixtures import new_doc_parser

TemplateTestCase = NamedTuple(
    "template_test",
    [("template", str),
     ("input_str", str),
     ("result", str),
     ("expectation", ContextManager),
     ("name", str)],
)

TemplateTestCases = [
    TemplateTestCase(template=r"(Словоерсы[\d]*Рев\-с)",
                     input_str="И скажем мы: Словоерсы12321Рев-с",
                     result="Словоерсы12321Рев-с",
                     expectation=does_not_raise(),
                     name="found_substr"),
    TemplateTestCase(template=r"Словоерсы[\d]*Рев\-с",
                     input_str="И промолчим мы",
                     result="",
                     expectation=does_not_raise(),
                     name="substr_not_found"),
    TemplateTestCase(template=r"Словоерсы[\d]*Рев\-с",
                     input_str="Словоерсы12321Рев-с",
                     result="",
                     expectation=does_not_raise(),
                     name="group_not_found"),
]


@pytest.mark.parametrize("case", TemplateTestCases, ids=case_names(TemplateTestCases))
def test_set_templates(new_doc_parser: Parser, case: TemplateTestCase):
    with case.expectation:
        assert new_doc_parser.extract_template(
            case.template, case.input_str) == case.result
