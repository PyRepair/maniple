To fix the bug in the pivot function, we need to modify the code where the columns parameter is checked. Instead of explicitly checking for None, we can use the `if columns` condition to raise an error if columns is not provided. This will ensure that a clearer error message is raised when columns is not specified.

Here's the fixed code:

```python
@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: "DataFrame", index=None, columns=None, values=None) -> "DataFrame":
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
    
    # Fix: Check if columns is not provided
    if not columns:
        raise ValueError("pivot() missing required argument: 'columns'")
    
    return indexed.unstack(columns)
```

This fix ensures that a `ValueError` is raised with the correct error message when `columns` is not provided.