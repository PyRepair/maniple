### Bug Analysis:
1. The `pivot_table` function is recursively calling itself when `aggfunc` is a list, resulting in multiple calls to pivot_table and potentially causing improper behavior.
2. The error is due to the expected return type being a DataFrame, but when aggregating on multiple functions simultaneously, a list is being constructed and concatenated, resulting in a Series object which causes the issue due to accessing columns.
3. The error originates from the inconsistent return data type when multiple aggregation functions are passed. The usage of `concat` on the results of multiple pivot_table calls results in a Series object without columns, leading to the attribute error 'Series' object has no attribute 'columns'.

### Bug Fix Strategy:
1. Modify the logic to correctly handle aggregation functions that are passed as a list, aggregating the results into a DataFrame rather than a Series.
2. When iterating through multiple functions, concatenate the pivot tables in a way that preserves the return type as DataFrame to avoid the `AttributeError`.

### Updated Corrected Function:
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
        pieces: Dict[str, DataFrame] = {}
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
            keys.append(getattr(func, "__name__", func))
            pieces[getattr(func, "__name__", func)] = table

        return concat(pieces, axis=1)

    keys = index + columns
    # Remaining logic remains the same...
```

This corrected version ensures that when aggregating multiple functions, the results are collected into a dictionary and then concatenated into a DataFrame rather than directly attempting to concatenate into a Series. This modification should resolve the attribute error issue.