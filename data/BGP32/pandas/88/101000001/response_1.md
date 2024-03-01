The bug in the provided function `pivot_table` is due to the recursive call to the same function within the loop where `pieces` are being appended. This recursive call causes an infinite loop resulting in a `RecursionError`. The issue arises from the fact that the function `pivot_table` is called within its own definition, leading to an infinite recursion.

To fix this bug, we need to ensure that the recursive call is avoided. One way to do this is by creating a separate function that can handle the aggregation for multiple functions instead of calling `pivot_table` recursively. This function can be responsible for aggregating the results and returning the combined dataframe.

Here is the corrected version of the `pivot_table` function:

```python
from pandas import concat

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
            keys.append(getattr(func, "__name__", func))

        grouped = data.groupby(index + columns, observed=observed)
        agged = grouped.agg(aggfunc)
        if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
            agged = agged.dropna(how="all")

            # Down cast if necessary
            for v in agged.columns:
                if is_integer_dtype(data[v]) and not is_integer_dtype(agged[v]):
                    agged[v] = maybe_downcast_to_dtype(agged[v], data[v].dtype)

        pieces.append(agged)

        return concat(pieces, keys=keys, axis=1)

    values_passed = values is not None
    if not values_passed:
        values = data.columns

    # Rest of the original pivot_table function code below...

```

In the corrected version, the logic for handling multiple aggregation functions has been modified to aggregate the data correctly without calling `pivot_table` recursively, thus preventing the infinite loop issue. 

This corrected function will help in avoiding the infinite recursion problem and provide the appropriate aggregation result for different functions specified.