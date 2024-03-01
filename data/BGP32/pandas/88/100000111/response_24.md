### Bug Explanation:
The bug lies in the logic where the function handles multi-index columns. When the columns parameter is passed as a tuple (for multi-index columns), the function fails to pivot the table correctly and causes an AttributeError when trying to access `table.columns` correctly.

### Bug Fix Strategy:
To fix the bug, we need to adjust the handling of multi-index columns to ensure that the extracted table retains a DataFrame structure even for multi-index cases.

### Updated Function:
Here is the corrected version of the `pivot_table` function:

```python
from pandas import Index, DataFrame, MultiIndex

# this is the corrected function
@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot_table"], indents=1)
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
        ...
        # existing code for handling list of aggfuncs

    keys = index + columns

    values_passed = values is not None
    if values_passed:
        ...
        # existing code for handling values

    else:
        ...

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)
    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        ...

    table = agged
    if table.index.nlevels > 1:
        ...
        # existing code for unstacking when index has multiple levels

    if not dropna:
        ...

    if isinstance(table, ABCDataFrame):
        ...
        # existing code for sorting columns when the table is a DataFrame

    if fill_value is not None:
        ...

    if margins:
        ...

    if values_passed and not values_multi and not table.empty and table.columns.nlevels > 1:
        table = table.loc[:, values]

    if len(index) == 0 and len(columns) > 0:
        table = table.T

    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
```

This corrected version of the function should now handle multi-index columns correctly and prevent the AttributeError when accessing `table.columns` for such cases.