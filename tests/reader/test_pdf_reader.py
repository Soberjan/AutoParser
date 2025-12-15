from typing import ContextManager, NamedTuple
from contextlib import nullcontext as does_not_raise

import pytest
import os

from helpers import case_names
from src.reader.pdf_reader import PDFReader

def test_pdf_reader():
    reader = PDFReader()
    output = reader.read_file('tests/test_data/reader_tests/doc3.pdf')
    assert output == 'Then she pulled out a fenis'
    
    output = reader.read_dir('tests/test_data/reader_tests')
    assert output == ['Then she pulled out a fenis']