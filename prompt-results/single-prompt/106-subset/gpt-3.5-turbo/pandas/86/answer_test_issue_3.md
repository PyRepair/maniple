After analyzing the issue, it seems that the error message is not being raised correctly when `columns=None` is used in `df.pivot`. To fix this issue, we can modify the code to explicitly raise an error when `columns` is `None`. Here's the fixed code snippet:

``` python
@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: "DataFrame", index=None, columns=None, values=None) -> "DataFrame":
    if columns is None:
        raise ValueError("The 'columns' parameter must be specified in df.pivot")
    
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

Now, when `columns` is `None`, a `ValueError` will be raised with a descriptive error message indicating that `columns` must be specified.

This fix ensures that the error message is raised correctly and provides clear instructions to the user on how to address the issue.