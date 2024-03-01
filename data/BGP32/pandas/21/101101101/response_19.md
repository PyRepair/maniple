The bug in the `_get_with` function lies in incorrectly handling the case where the `key` is a scalar. The function should use `self.loc[key]` for scalar keys instead of trying to infer the type and then decide whether to use `self.loc` or `self.iloc`.

To fix this bug, we can modify the code to always use `self.loc[key]` for scalar keys. Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    # Handle scalar keys
    if is_scalar(key):
        return self.loc[key]
    
    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By making this change, the corrected function will handle scalar keys appropriately and pass the failing test cases provided.