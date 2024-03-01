### Bug Explanation
The bug occurs because the function `dispatch_to_series` encounters an issue when trying to perform an operation involving a NumPy array and a 'NaTType' object. The error message `TypeError: unsupported operand type(s) for *: 'numpy.ndarray' and 'NaTType'` is raised because the function does not handle this case correctly.

### Bug Fix Strategy
To fix this bug, we need to update the `column_op` function inside the `dispatch_to_series` function to handle the case where the right operand is a 'NaTType' object. We should check for this case and apply the operation appropriately.

### Corrected Function
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
            return {i: func(a.iloc[:, i], b.iloc[i]) if not pd.isnull(b.iloc[i]) else pd.NaT for i in range(len(a.columns))}

    elif isinstance(right, ABCSeries):
        assert right.index.equals(left.index)

        def column_op(a, b):
            return {i: func(a.iloc[:, i], b) if not pd.isnull(b) else pd.NaT for i in range(len(a.columns))}

    else:
        raise NotImplementedError(right)

    new_data = expressions.evaluate(column_op, str_rep, left, right)
    return new_data
```

By adding checks for 'NaTType' objects and handling them appropriately in the `column_op` function, the corrected version of the function should now be able to perform operations involving NumPy arrays and 'NaTType' objects without raising errors.