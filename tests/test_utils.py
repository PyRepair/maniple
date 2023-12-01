import pytest
from LLMRepair.utils import generate_contextual_diff_with_char_limit


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
