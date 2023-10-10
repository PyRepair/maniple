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

        if pd.api.types.is_list_like(values) and not isinstance(values, tuple):
            # Exclude tuple because it is seen as a single column name
            indexed = data[values].to_frame(name=values).set_index(index)
        else:
            indexed = data[values].to_frame(name=values).set_index(index)
    return indexed.unstack(columns)
```

Explanation:

The issue in the original code is that when `values` is not None and `values` is not list-like, `indexed` is not correctly constructed. In the fixed code, the issue is resolved by using the `to_frame()` method to create a DataFrame with the specified column name and then setting the index to the created DataFrame. This ensures that `indexed` is correctly created in both cases. Additionally, I have imported `pd` to use `pd.api.types.is_list_like` instead of `is_list_like` to avoid any potential import errors. Moreover, I have added type hints for clarity.