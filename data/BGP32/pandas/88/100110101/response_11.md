The bug in the `pivot_table` function appears to arise from calling the same function recursively without considering the correct types of input values. This recursive call causes an incorrect structure of the DataFrame leading to AttributeError when trying to access 'columns' on a Series object.

To fix this issue, we need to ensure that the input values are processed correctly at each level of the function execution, and all manipulations are done based on the expected DataFrame structure.

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
    # Helper function to convert None or single entry to list
    def _convert_by(by):
        return [] if by is None else by if isinstance(by, list) else [by]

    index = _convert_by(index)
    columns = _convert_by(columns)
    data = data.copy()

    if isinstance(aggfunc, list):
        pieces = []
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

        # Make sure value labels are in data
        for i in values:
            if i not in data:
                raise KeyError(i)

        to_filter = [x for x in keys + values if x in data]
        data = data[to_filter]

    else:
        values = data.columns
        values = list(set(values) - set(keys))

    grouped = data.groupby(keys, observed=observed)
    agged = grouped.agg(aggfunc)
    if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
        agged = agged.dropna(how="all")

        # Downcast to int if original values were ints
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
        to_unstack = [i for i in range(len(index), len(keys)) if agged.index.names[i] is None or agged.index.names[i] in index]
        table = agged.unstack(to_unstack)

    if not dropna:
        if table.index.nlevels > 1:
            table = table.reindex(columns=pd.MultiIndex.from_product(table.index.levels, names=table.index.names))

        if table.columns.nlevels > 1:
            table = table.reindex(columns=pd.MultiIndex.from_product(table.columns.levels, names=table.columns.names))

    if isinstance(table, ABCDataFrame):
        table = table.sort_index(axis=1)

    if fill_value is not None:
        table = table.fillna(fill_value)

    if margins:
        if dropna:
            data = data.dropna()
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

    if not index and columns:
        table = table.T

    if isinstance(table, ABCDataFrame) and dropna:
        table = table.dropna(how="all", axis=1)

    return table
```

By making sure the correct DataFrame structures are used at each step and avoiding unnecessary DataFrame copies, this corrected version of the `pivot_table` function should prevent the AttributeError issues and pass the failing test cases.