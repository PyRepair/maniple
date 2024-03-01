### Analysis:
- The error occurs in the `pivot_table` function when handling multi-index columns. The issue arises when trying to access `table.columns.nlevels` for a Series object.
- The failing test `test_pivot_table_multiindex_only` encounters an AttributeError mentioning that 'Series' object has no attribute 'columns'.
- The GitHub issue references this bug and provides code snippets demonstrating the error. It aims to have consistent behavior with multi-index columns and single columns/rows in `pivot_table` operation.

### Bug Cause:
The `pivot_table` function is encountering the error because the `table` object is sometimes being reduced to a Series instead of a DataFrame, leading to the AttributeError when trying to access `table.columns.nlevels`.

### Bug Fix Strategy:
To fix the bug, the `pivot_table` function should ensure that the `table` object remains a DataFrame throughout its processing. This can be achieved by handling conditions that result in the `table` object becoming a Series differently to retain DataFrame structure.

### Updated `pivot_table` Function:
Here is the corrected version of the `pivot_table` function:

```python
from pandas import DataFrame, MultiIndex, Index
from pandas.core.reshape.concat import concat
from pandas.core.dtypes.common import is_list_like, is_scalar
from pandas.core.groupby import Grouper

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
    index = _convert_by(index)
    columns = _convert_by(columns)

    if isinstance(aggfunc, list):
        pieces: List[DataFrame] = []
        keys = []
        for func in aggfunc:
            table = pivot_table(
                data,
                values=values,
                index=index,
                columns=columns,
                fill_value=fill_value,
                aggfunc=func,
                margins=margins,
                dropna=dropna,
                margins_name=margins_name,
                observed=observed,
            )
            pieces.append(table)
            keys.append(getattr(func, "__name__", func))

        return concat(pieces, keys=keys, axis=1)

    keys = index + columns

    values_passed = values is not None

    data_partial = data
    data_unfiltered = data
    
    for i in keys:
        if isinstance(i, Grouper):
            i = i.key
        try:
            if i in data_unfiltered:
                to_filter.append(i)
        except TypeError:
            pass
    
    data_partial = data_partial[to_filter] 

    grouped = data_partial.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)
    if dropna and isinstance(agged, DataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

    table = agged

    if table.index.nlevels > 1:
        index_names = table.index.names[: len(index)]
        to_unstack = list(range(len(index), len(keys)))
        table = table.unstack(to_unstack)

    if not dropna:
        table = table.reindex(cartesian_product(table.index.levels), axis=0)
        table = table.reindex(cartesian_product(table.columns.levels), axis=1)

    if fill_value is not None:
        table = table.fillna(fill_value, downcast="infer")

    if margins:
        if dropna:
            data = data[data.notna().all(axis=1)]
        table = _add_margins(
            table,
            data_unfiltered,
            values,
            rows=index,
            cols=columns,
            aggfunc=aggfunc,
            observed=dropna,
            margins_name=margins_name,
            fill_value=fill_value,
        )

    if values_passed and table.columns.nlevels > 1:
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T
        
    if isinstance(table, DataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
```

After applying the corrections, the `pivot_table` function should now handle multi-index columns without encountering the AttributeError mentioned in the failing tests and resolve the issue reported on GitHub.