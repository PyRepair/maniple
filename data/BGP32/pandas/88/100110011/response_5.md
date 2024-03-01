### Analysis:
The `pivot_table` function is failing when attempting to pivot a DataFrame with multi-index columns only. The error occurs due to a `Series` object being returned instead of a `DataFrame`, leading to an attribute error.

### Bugs:
1. The recursive call to `pivot_table` within the function creates nested `DataFrame` instances instead of directly aggregating the results.
2. The code does not correctly handle the case when only multi-index columns are passed to the `pivot_table` function, leading to a `Series` object instead of a `DataFrame`.
3. Nested handling of index names is causing issues with unstacking.

### Fixes:
1. Replace the recursive call to `pivot_table` with direct aggregation of results when working with multiple aggregation functions.
2. Directly handle the case when only multi-index columns are passed to the `pivot_table` function to ensure a `DataFrame` is returned in all cases.
3. Simplify the handling of index names for unstacking to avoid issues with naming.

### Corrected Version:
```python
from pandas.core.frame import DataFrame
from pandas.core.reshape.concat import concat
from pandas.core.series import Series
from pandas.core.indexes.api import Index, MultiIndex
from pandas.core.generic import ABCDataFrame

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
) -> DataFrame:
    keys = index + columns

    if isinstance(aggfunc, list):
        pieces: List[DataFrame] = []
        keys = []
        for func in aggfunc:
            agged = data.groupby(keys, observed=observed).agg(func)
            agged = agged.unstack(level=[-1] * len(columns))
            pieces.append(agged)
            keys.append(getattr(func, "__name__", func))

        table = concat(pieces, axis=1, keys=keys)

    else:
        grouped = data.groupby(keys, observed=observed)
        agged = grouped.agg(aggfunc)
        table = agged

    if dropna and isinstance(table, ABCDataFrame) and not table.empty:
        table = table.dropna(how="all")

    if fill_value is not None:
        table = table.fillna(fill_value)

    if margins:
        table = _add_margins(
            table,
            data,
            values,
            rows=index,
            cols=columns,
            aggfunc=aggfunc,
            observed=dropna,
            margins_name=margins_name,
            fill_value=fill_value,
        )

    if isinstance(table, Series):
        table = table.to_frame()

    return table
``` 

The corrected version of the `pivot_table` function directly handles aggregation functions without recursion, ensures the correct return type is a `DataFrame`, and simplifies the handling of multi-index columns.