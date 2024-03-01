The bug in the `_get_with` function is that it incorrectly handles the key type when it is a list, NumPy array, or Index, causing a KeyError to be raised instead of handling the key properly.

To fix this bug, we need to properly handle the case where the key is a list, NumPy array, or Index by converting it to a list and then proceed with the appropriate operations.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    key = ensure_index(key)
    
    if isinstance(key, list):
        key_type = lib.infer_dtype(key, skipna=False)
    else:
        key = [key]
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

This corrected version ensures that the key is handled correctly when it is a list, NumPy array, or Index.

The function should now pass the failing test cases provided.