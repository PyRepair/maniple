import pytest
from LLMRepair.utils import (
    generate_contextual_diff_with_char_limit,
    extract_function_from_response,
)


def test_generate_contextual_diff_with_char_limit():
    # Define test inputs
    input1 = "some input"
    input2 = "some other input"
    char_limit = 100

    # Call the function with the test inputs
    result = generate_contextual_diff_with_char_limit(input1, input2, char_limit)

    # Define the expected output
    expected_output = "-some input\n+some other input"

    # Assert that the function output is as expected
    assert result == expected_output


def test_extract_function_with_imports():
    # Define test inputs
    input_code = """
import os

def test_function():
    print(os.getcwd())
    """

    # Call the function with the test inputs
    result = extract_function_from_response(input_code, "test_function")

    # Define the expected output
    expected_output = """
def test_function():
    import os
    print(os.getcwd())
    """

    # Assert that the function output is as expected
    assert result.strip() == expected_output.strip()


def test_extract_function_from_class():
    input_code = """
class Driver(object):
    # ... omitted code ...

    def _partially_consume_prefix(self, prefix, column):
        '''docstring'''
        lines = []
        current_line = ""
"""

    expected_output = """
def _partially_consume_prefix(self, prefix, column):

    '''docstring'''
    lines = []
    current_line = ""
"""

    result = extract_function_from_response(input_code, "_partially_consume_prefix")
    assert result.strip() == expected_output.strip()
