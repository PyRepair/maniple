```python
@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: "DataFrame", index=None, columns=None, values=None) -> "DataFrame":
    if columns is not None:  # Fix: Check if columns is not None
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
    else:
        raise ValueError("'columns' cannot be None")  # New: Raise value error if columns is None
```