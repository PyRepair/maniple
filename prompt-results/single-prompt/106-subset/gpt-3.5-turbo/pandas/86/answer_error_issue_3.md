To fix the bug, we need to modify the code to raise a `TypeError` with a custom error message when the `columns` parameter is `None`. 

Here is the fixed code:
```python
from pandas.core.frame import DataFrame
from pandas.core.indexes.base import is_list_like, MultiIndex

def pivot(data: "DataFrame", index=None, columns=None, values=None) -> "DataFrame":
    if columns is None:
        raise TypeError("columns is a required argument")

    if values is None:
        cols = [columns] if index is None else [index, columns]
        append = index is None
        indexed = data.set_index(cols, append=append)
    else:
        if index is None:
            index = data.index
        else:
            index = data[index]
        index = MultiIndex.from_arrays([index, data[columns]])

        if is_list_like(values) and not isinstance(values, tuple):
            # Exclude tuple because it is seen as a single column name
            indexed = data._constructor(
                data[values].values, index=index, columns=values
            )
        else:
            indexed = data._constructor_sliced(data[values].values, index=index)
    return indexed.unstack(columns)
```

With this fixed code, when `columns` is `None`, a `TypeError` will be raised with the message "columns is a required argument", instead of a `KeyError`.