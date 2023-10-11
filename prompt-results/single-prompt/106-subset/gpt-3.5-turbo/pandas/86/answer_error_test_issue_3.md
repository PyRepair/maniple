```python
from typing import Optional, Union

@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: "DataFrame", index: Optional[Union[str, object]] = None, columns: Union[str, object] = None, values: Optional[str] = None) -> "DataFrame":
    if columns is None:
        raise ValueError("pivot() missing 1 required argument: 'columns'")
        
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

The issue occurred because the `columns` parameter was not properly handled in the function. I have added a check at the beginning of the function to ensure that the `columns` parameter is not `None`. If it is `None`, a `ValueError` is raised with the appropriate error message.