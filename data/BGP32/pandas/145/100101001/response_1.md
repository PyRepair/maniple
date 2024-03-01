### Bug Explanation
The bug in the `dispatch_to_series` function arises from the incorrect implementation of the `column_op` function for handling the case where `right` is a Series and `axis` is set to `'columns'`. In this case, the function is supposed to perform the operation row-by-row, but the existing implementation is performing it column-by-column, leading to incorrect results.

### Bug Location
The bug is located in the following section of the `dispatch_to_series` function:
```python
elif isinstance(right, ABCSeries) and axis == "columns":
    assert right.index.equals(left.columns)

    def column_op(a, b):
        return {i: func(a.iloc[:, i], b.iloc[i]) for i in range(len(a.columns))}
```

### Fix Strategy
To fix the bug, we need to modify the `column_op` function when `right` is a Series and `axis` is set to `'columns'` to iterate over the rows instead of the columns.

### Corrected Version
```python
def dispatch_to_series(left, right, func, str_rep=None, axis=None):
    """
    Evaluate the frame operation func(left, right) by evaluating
    column-by-column, dispatching to the Series implementation.

    Parameters
    ----------
    left : DataFrame
    right : scalar or DataFrame
    func : arithmetic or comparison operator
    str_rep : str or None, default None
    axis : {None, 0, 1, "index", "columns"}

    Returns
    -------
    DataFrame
    """
    import pandas.core.computation.expressions as expressions

    right = lib.item_from_zerodim(right)
    if lib.is_scalar(right) or np.ndim(right) == 0:

        def column_op(a, b):
            return {i: func(a.iloc[:, i], b) for i in range(len(a.columns))}

    elif isinstance(right, ABCDataFrame):
        assert right._indexed_same(left)

        def column_op(a, b):
            return {i: func(a.iloc[:, i], b.iloc[:, i]) for i in range(len(a.columns))}

    elif isinstance(right, ABCSeries) and axis == "columns":
        assert right.index.equals(left.columns)

        def column_op(a, b):
            return {i: func(a.iloc[i], b.iat[i]) for i in range(len(a))}

    elif isinstance(right, ABCSeries):
        assert right.index.equals(left.index)

        def column_op(a, b):
            return {i: func(a.iloc[:, i], b) for i in range(len(a.columns))}

    else:
        raise NotImplementedError(right)

    new_data = expressions.evaluate(column_op, str_rep, left, right)
    return new_data
```

By modifying the `column_op` function to iterate over rows when `right` is a Series and `axis` is set to `'columns',` the corrected version of the function should now provide the expected results for the failing test.