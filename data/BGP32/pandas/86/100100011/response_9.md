### Analysis:
- The `pivot` function is designed to accept `index`, `columns`, and `values` as arguments.
- The failing test is expecting an error to be raised when the `columns` argument is missing.
- The bug occurs when `columns` is not provided explicitly, leading to the wrong error message being raised.

### Bug Explanation:
- In the original implementation, there is no explicit check for the presence of the `columns` argument, causing confusion when it is missing.
- The function mistakenly allows `columns` to be `None`, which doesn't align with the intended behavior of the function.
- This results in the error message being misleading and causing confusion for users when `columns=None`.

### Fix Strategy:
- Add a check to ensure that `columns` is provided when calling the `pivot` function.
- Raise a `TypeError` explicitly if `columns` is not provided.
- Update the error message to indicate that `columns` is a required argument.

### Corrected Version:
```python
@Substitution("\ndata : DataFrame")
@Appender(_shared_docs["pivot"], indents=1)
def pivot(data: "DataFrame", index=None, columns=None, values=None) -> "DataFrame":
    if columns is None:  # Check if 'columns' is not provided
        raise TypeError("pivot() missing 1 required argument: 'columns'")  # Raise error explicitly

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

### Summary:
- The corrected version of the `pivot` function now explicitly checks for the presence of the `columns` argument.
- If `columns` is missing, a `TypeError` is raised with a clear error message.
- This fix ensures that the function behaves as expected and passes the failing test, resolving the issue raised on GitHub.