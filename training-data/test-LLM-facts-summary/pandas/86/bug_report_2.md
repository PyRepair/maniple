Facts for Bug Report:
1. The error message raised when calling df.pivot with columns=None is confusing and should indicate that columns is not optional.
2. According to the docstring, the columns parameter is required, while index and values are optional.
3. The failing test function df.pivot_columns_none_raise_error() in test_pivot.py raises a TypeError with a confusing error message.
4. The error message raised indicates a KeyError related to the None value for columns, which does not clearly convey that columns is a required parameter.

These facts are useful because they provide information on the expected behavior of the pivot function, the specific scenario that triggers the bug, and the confusing error message that needs to be addressed.