from typing import ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise

import pytest
import os

from helpers import case_names
from src.reader.docx_reader import DOCXReader

def test_docx_reader():
    reader = DOCXReader()
    output = reader.read_file('tests/test_data/reader_tests/doc2.docx')
    assert output == 'Said girl you look fine\n'
    
    output = reader.read_dir('tests/test_data/reader_tests')
    assert output == ['Said girl you look fine\n']