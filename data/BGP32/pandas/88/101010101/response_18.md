### Bug Analysis
The bug occurs due to the function trying to access the `columns` attribute on a Series object. The `Series` object does not have a `columns` attribute, which results in an `AttributeError`.

### Bug Fix Strategy
To fix this bug, we need to ensure that the `table` variable is always a DataFrame before attempting to access its `columns` attribute.

### Updated Function
Here is the corrected version of the `pivot_table` function:

```python
import pandas as pd
from pandas.util._decorators import Appender, Substitution
from pandas.core.frame import _shared_docs
from pandas.core.reshape.concat import concat
from pandas.core.groupby import Grouper
from pandas.core.reshape.util import cartesian_product
from pandas import DataFrame

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
    if values_passed:
        if is_list_like(values):
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
    if dropna and isinstance(agged, pd.DataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

    table = agged
    if isinstance(table, pd.DataFrame) and table.index.nlevels > 1:
        index_names = agged.index.names[: len(index)]
        to_unstack = [i for i in range(len(index), len(keys) + len(index))]
        table = agged.unstack(to_unstack)

    if not dropna:
        if table.index.nlevels > 1:
            m = pd.MultiIndex.from_arrays(
                cartesian_product(table.index.levels), names=table.index.names
            )
            table = table.reindex(m, axis=0)

        if table.columns.nlevels > 1:
            m = pd.MultiIndex.from_arrays(
                cartesian_product(table.columns.levels), names=table.columns.names
            )
            table = table.reindex(m, axis=1)

    if isinstance(table, pd.DataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table.fillna(fill_value)

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

    if values_passed and not values_multi and not table.empty and (table.columns.nlevels > 1):
        table = table[values[0]]

    if len(index) == 0 and len(columns) > 0:
        table = table.T

    if isinstance(table, pd.DataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
```

By modifying the code as described above, the corrected `pivot_table` function should now correctly handle the cases provided and avoid the `AttributeError` that occurred previously.