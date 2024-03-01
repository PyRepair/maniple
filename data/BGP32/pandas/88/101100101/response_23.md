### Bug Analysis:
The bug occurs when the pivot_table function is called recursively with a list of aggfunc values. Inside the recursive call, a concat function is used to combine the results of each aggregation function into a DataFrame. However, the function tries to access the name of the aggregation function using getattr(func, "__name__", func), which does not work correctly when func is a string.

### Bug Fix:
To fix the bug, we need to modify the code that handles the list of aggfunc values. Specifically, we need to check if the aggfunc is a string before trying to access its name. We can achieve this by modifying the code to use isinstance(func, str) instead of trying to access __name__ attribute.

### Corrected Function:
```python
from pandas.core.reshape.util import cartesian_product

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
            keys.append(func if isinstance(func, str) else getattr(func, "__name__", func))

        return concat(pieces, keys=keys, axis=1)

    # Rest of the function remains unchanged
```

By making this modification, the function should now correctly handle the list of aggfunc values and concatenate the results into a DataFrame without causing the attribute error.