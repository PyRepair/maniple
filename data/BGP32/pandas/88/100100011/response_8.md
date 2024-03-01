Looking at the provided function `pivot_table` and the failing test `test_pivot_table_multiindex_only`, the bug seems to be related to handling multi-index columns. The failing test aims to test the behavior of `pivot_table` when using multi-index columns but the implementation of the function does not handle this case correctly which leads to an `AttributeError` when trying to access the `columns` attribute of a `Series`.

### Cause of the Bug:
- The bug is caused when the `pivot_table` function is handling multi-index columns.
- In the failing test, the `pivot_table` is called with `values='v'` and `columns=cols`, where `cols` is a tuple representing two columns that should be part of the multi-index.
- The buggy implementation does not properly handle this scenario and tries to access the `columns` attribute of the result `table`, which leads to an `AttributeError` as the result could be a `Series` instead of a `DataFrame` with columns.

### Strategy for Fixing the Bug:
- The bug can be fixed by ensuring that the function handles the case of multi-index columns appropriately and returns a `DataFrame` with columns.
- Modify the code to check if the result is a `Series` and handle this case by converting it into a single-row DataFrame or handle it in a way that preserves the necessary structure.

### Corrected Version of the `pivot_table` function:
Here is the corrected version of the `pivot_table` function:

```python
def pivot_table(
    data,
    values=None,
    index=None,
    columns=None,
    aggfunc="mean",
    fill_value=None,
    margins=False,
    dropna=True,
    margins_name="All",
    observed=False,
) -> "DataFrame":
    index = _convert_by(index)
    columns = _convert_by(columns)

    table = data.pivot_table(
        values=values,
        index=index,
        columns=columns,
        aggfunc=aggfunc,
        fill_value=fill_value,
        margins=margins,
        dropna=dropna,
        margins_name=margins_name,
        observed=observed,
    )

    # Ensure the result is a DataFrame with columns
    if isinstance(table, ABCSeries):
        table = table.to_frame().T

    return table
```

In this corrected version, `pivot_table` function leverages the `pivot_table` method directly on the `data` DataFrame, which inherently handles multi-index columns correctly. Then, we check if the result is a `Series` and convert it into a single-row DataFrame to avoid the Attribute Error encountered in the failing test.