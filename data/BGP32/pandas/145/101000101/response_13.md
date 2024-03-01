The bug in the `dispatch_to_series` function arises from incorrect handling of the input parameters and construction of the `column_op` function based on the type of `right`. The function is not correctly dispatching to the appropriate operation based on the type of `right`.

### Bug Explanation:
- When `right` is a scalar or a DataFrame, the function constructs `column_op` to perform the operation between each column of `left` and `right`.
- If `right` is an ABCSeries and `axis` is set to `'columns'`, the function constructs `column_op` to operate row-by-row.
- However, irrespective of the type of `right`, when `right` is an ABCSeries and `axis` is not `'columns'`, the function constructs `column_op` to operate column-by-column. This leads to incorrect behavior.

### Fix Strategy:
To fix the bug, when `right` is an ABCSeries and `axis` is not `'columns'`, the function should construct `column_op` to perform the operation element-wise on each corresponding element of the columns. This will ensure that the operation is correctly applied across the columns based on the type of `right`.

### Corrected Function:
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

        column_op = lambda a, b: {i: func(a.iloc[:, i], b) for i in range(len(a.columns))}

    elif isinstance(right, ABCDataFrame):
        assert right._indexed_same(left)

        column_op = lambda a, b: {i: func(a.iloc[:, i], b.iloc[:, i]) for i in range(len(a.columns))}

    elif isinstance(right, ABCSeries) and axis == "columns":
        assert right.index.equals(left.columns)

        column_op = lambda a, b: {i: func(a.iloc[:, i], b.iloc[i]) for i in range(len(a.columns))}

    elif isinstance(right, ABCSeries):
        assert right.index.equals(left.index)

        column_op = lambda a, b: {i: func(a.iloc[:, i], b.iloc[i]) for i in range(len(a.columns))}

    else:
        raise NotImplementedError(right)

    new_data = expressions.evaluate(column_op, str_rep, left, right)
    return new_data
```

By correctly defining `column_op` based on the type of `right` and `axis`, the function will now dispatch the operation appropriately and return the expected results for the given test cases.