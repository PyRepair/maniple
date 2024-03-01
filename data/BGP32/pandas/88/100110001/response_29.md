### Bug Analysis:
The `pivot_table` function is recursively calling itself when `aggfunc` is a list of functions. However, during this recursion, the returned `table` object is not being checked for its type, leading to a situation where it can be a Series instead of a DataFrame. This makes the subsequent operations on `table.columns` trigger an AttributeError because a Series object does not have a `columns` attribute.

#### Error Cause:
1. The recursive call to `pivot_table` when `aggfunc` is a list of functions.
2. Lack of type checking on the returned `table` object in the recursive call.
3. Failure to handle the case when `table` is a Series instead of a DataFrame.

### Bug Fix Strategy:
1. When a DataFrame is expected in the returned `table` object, it should be explicitly checked for its type.
2. If `table` is a Series, it should be converted to a DataFrame to ensure the subsequent operations succeed.

### Bug Fix Code:
```python
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
            # Check if returned table is a Series and convert to DataFrame
            if isinstance(table, ABCSeries):
                table = table.to_frame().T

            pieces.append(table)
            keys.append(getattr(func, "__name__", func))

        return concat(pieces, keys=keys, axis=1)

    keys = index + columns
    ...
```

By explicitly checking if the returned `table` is a Series in the recursive call and converting it to a DataFrame if needed, the bug should be fixed, and the function should return correct results for multi-index pivot tables.