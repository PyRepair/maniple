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


def test_extract_function_from_pure_function_file():
    input_code = """
def pivot(data: "DataFrame", index=None, columns, values) -> "DataFrame":
    if columns is None:
        raise TypeError("pivot() missing 1 required argument: 'columns'")

    if values is None:
        cols = [columns] if index is None else [index, columns]
        append = index is None
        indexed = data.set_index(cols, append=append)
    else:
        if index is None:
            index = data.index
        else:
            index = data[index]
        index = MultiIndex.from_arrays([index, data[columns]])

        if is_list_like(values) and not isinstance(values, tuple):
            # Exclude tuple because it is seen as a single column name
            indexed = data._constructor(
                data[values].values, index=index, columns=values
            )
        else:
            indexed = data._constructor_sliced(data[values].values, index=index)
    return indexed.unstack(columns)
"""
    with pytest.raises(SyntaxError):
        extract_function_from_response(input_code, "pivot")
