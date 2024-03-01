### Explanation
The bug in the function arises due to the fact that when the `aggfunc` parameter is a list, the function recursively calls itself. However, during the recursive call, it does not handle the returned result correctly, leading to an AttributeError on Series object.

The issue occurs when building the `table` DataFrame where the function gets the wrong column attribute on the Series object, leading to the AttributeError.

### Solution Strategy
The bug can be fixed by correctly handling the recursive call when `aggfunc` is a list. We need to ensure that the `table` DataFrame is constructed correctly during the recursive calls to `pivot_table()`.

The fix involves:
1. When `aggfunc` is a list, build a list of DataFrames `pieces` and a list of keys based on the function names.
2. After iterating over the aggregation functions and building the required pieces, concatenate the DataFrames in the `pieces` list and return the concatenated DataFrame with the respective keys.

Here is the corrected version of the function:

```python
def pivot_table(data, values=None, index=None, columns=None, aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All', observed=False) -> 'DataFrame':
    # Body of the function
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

    # The rest of the function remains the same
```

With this correction, the function will correctly handle the case where `aggfunc` is a list and avoid the AttributeError that was occurring before.