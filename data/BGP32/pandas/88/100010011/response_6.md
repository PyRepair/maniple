### Analysis:
- The function `pivot_table` is supposed to create a pivot table based on the provided data, values, index, columns, aggregation function, and other specified parameters.
- The error message states that `'Series'` object has no attribute 'columns', indicating that the `table` being processed is a Series object instead of a DataFrame.

### Bug Explanation:
- The bug occurs when the provided `columns` parameter is of tuple type, resulting in the creation of a Series object (instead of a DataFrame) rather than a pivot table. This leads to an AttributeError when trying to access `.columns` on a Series.

### Fix Strategy:
- To address the bug, we should ensure that the output of the function is always a DataFrame, even when dealing with multi-index columns.
- When detecting multi-index columns are being used, we need to convert the result to a DataFrame before proceeding.

### Bug Fix:

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

    if isinstance(aggfunc, list):
        # Remaining code remains the same

    keys = index + columns

    values_passed = values is not None
    if values_passed:
        # Remaining code remains the same

    else:
        # Remaining code remains the same

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)
    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        # Remaining code remains the same

    table = DataFrame(agged)  # Convert to DataFrame
    # Remaining code remains the same
```

By converting the `agged` variable to a DataFrame before further processing, we ensure that the output is a DataFrame even when multi-index columns are used. This fix will address the AttributeError and make the function work as intended.