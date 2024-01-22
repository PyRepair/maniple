Useful Facts:
1. The error message `KeyError: 'None of [None] are in the columns'` is confusing and not appropriate for this situation.
2. The docstring indicates that the `index` and `values` parameters can be optional in `df.pivot`, but `columns` is not optional.
3. The failing test function `test_pivot_columns_none_raise_error` provides a clear example and expectation for the behavior of the `pivot` function.
4. The source code checks for the `values` parameter to determine how to handle the `index` parameter, but does not enforce the requirement for the `columns` parameter.