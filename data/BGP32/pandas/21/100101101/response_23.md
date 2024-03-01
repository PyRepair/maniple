The issue in the provided `_get_with` function lies in the logic for handling non-list-like keys. The bug causes a wrong type inference for the `key_type`, leading to incorrect behavior when trying to index the Series.

Here's a strategy to fix the bug:
1. Modify the logic for non-list-like keys to correctly handle the cases where the key is a scalar or an ndarray.
2. Ensure that the key_type is inferred correctly based on the input type.
3. Adjust the return statement based on the inferred key_type to properly index the Series.

Here's the corrected version of the `_get_with` function:

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

    if is_scalar(key) or isinstance(key, np.ndarray):
        key = [key]

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

With this corrected version, the issue with failing tests should be resolved, and the function should handle non-list-like keys properly to infer the key type correctly and index the Series accordingly.