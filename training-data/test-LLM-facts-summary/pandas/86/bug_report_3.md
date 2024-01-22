Useful facts to include in the bug report:

1. The error message is "KeyError: 'None of [None] are in the columns'" when columns=None is passed to df.pivot, which is confusing and incorrect.
2. According to the documentation, index and values can be optional in df.pivot, but columns is not optional.
3. The failing test function 'test_pivot_columns_none_raise_error' in the test file 'test_pivot.py' provides a specific example of when the bug occurs.
4. The bug occurs in the 'pivot' function defined in the file 'pandas/core/reshape/pivot.py'.
5. The bug is causing a wrong error message to be raised when columns=None is passed to df.pivot.