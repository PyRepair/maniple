The cause of the bug in the provided function is due to the logic inside the `else` block when `values` is not None. The bug occurs because the `index` and `columns` variables are not properly handled and constructed as expected, leading to incorrect data manipulation. 

To fix the bug, we need to correct the creation of the `index` variable using the `MultiIndex.from_arrays` method and ensure that the data is structured correctly before being returned.

Here is the corrected version of the function:

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
        
        # Construct MultiIndex from arrays
        index = MultiIndex.from_arrays([data[index], data[columns]])
        
        if is_list_like(values) and not isinstance(values, tuple):
            # Exclude tuple because it is seen as a single column name
            indexed = data._constructor(data[values].values, index=index, columns=values)
        else:
            indexed = data._constructor_sliced(data[values].values, index=index)
    
    return indexed.unstack(columns)
```

This corrected version properly constructs the `index` variable using `MultiIndex.from_arrays` and ensures that the data is structured correctly before unstacking columns.