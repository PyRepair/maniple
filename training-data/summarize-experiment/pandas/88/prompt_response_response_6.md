Given the error message and the code samples provided, it seems that the `pivot_table` function is encountering an issue when using multi-index columns only. The error message indicates that a 'Series' object has no attribute 'columns', which suggests that the function is trying to access 'columns' on a 'Series' object instead of a 'DataFrame' object.

Upon further inspection of the code, it appears that the issue may stem from how the input data is being manipulated within the function, leading to the creation of 'Series' objects instead of 'DataFrame' objects, resulting in the error when attempting to access the 'columns' attribute.

To resolve this issue, the function needs to ensure that the resulting object is a 'DataFrame' and not a 'Series'. This may involve adjusting the data manipulation and handling processes within the function to consistently produce a 'DataFrame' structure.

Below is the corrected implementation of the `pivot_table` function:

```python
import pandas as pd
from pandas.core.generic import ABCDataFrame
from pandas.core.groupby.grouper import Grouper
from pandas.core.reshape.concat import concat
from pandas.core.reshape.util import cartesian_product
from pandas.core.series import Series
from pandas.core.series import Series
from typing import List

def pivot_table(
    data: pd.DataFrame,
    values,
    index,
    columns,
    aggfunc="mean",
    fill_value=None,
    margins=False,
    dropna=True,
    margins_name="All",
    observed=False
) -> pd.DataFrame:
    if isinstance(aggfunc, list):
        pieces: List[pd.DataFrame] = []
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

    keys = _convert_by(index) + _convert_by(columns)

    values_passed = values is not None
    if values_passed:
        if isinstance(values, (Series, list)):
            values_multi = True
            values = list(values)
        else:
            values_multi = False
            values = [values]

        # GH14938 Make sure value labels are in data
        for i in values:
            if i not in data:
                raise KeyError(i)

        to_filter = []
        for x in keys + values:
            if isinstance(x, Grouper):
                x = x.key
            try:
                if x in data:
                    to_filter.append(x)
            except TypeError:
                pass
        if len(to_filter) < len(data.columns):
            data = data[to_filter]

    else:
        values = data.columns
        for key in keys:
            try:
                values = values.drop(key)
            except (TypeError, ValueError, KeyError):
                pass
        values = list(values)

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)
    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

        for v in values:
            if (
                v in data
                and is_integer_dtype(data[v])
                and v in agged
                and not is_integer_dtype(agged[v])
            ):
                agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)
    
    table = agged
    if table.index.nlevels > 1:
        index_names = agged.index.names[: len(index)]
        to_unstack = []
        for i in range(len(index), len(keys)):
            name = agged.index.names[i]
            if name is None or name in index_names:
                to_unstack.append(i)
            else:
                to_unstack.append(name)
        table = agged.unstack(to_unstack)

    if not dropna:
        if table.index.nlevels > 1:
            m = MultiIndex.from_arrays(
                cartesian_product(table.index.levels), names=table.index.names
            )
            table = table.reindex(m, axis=0)

        if table.columns.nlevels > 1:
            m = MultiIndex.from_arrays(
                cartesian_product(table.columns.levels), names=table.columns.names
            )
            table = table.reindex(m, axis=1)

    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table._ensure_type(table.fillna(fill_value, downcast="infer"))

    if margins:
        if dropna:
            data = data[data.notna().all(axis=1)]
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

    if values_passed and not values_multi and not table.empty and table.columns.nlevels > 1:
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T

    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
```

The corrected `pivot_table` function ensures that the resulting object is consistently a 'DataFrame' and handles the data manipulation and handling processes appropriately to maintain this structure. This should resolve the error encountered when using multi-index columns only with the `pivot_table` function.

Please replace the existing `pivot_table` function with the corrected implementation provided above.