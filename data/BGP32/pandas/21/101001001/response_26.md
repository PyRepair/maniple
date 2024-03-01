The bug in the `_get_with` function arises from the incorrect handling of the key type in different scenarios. The `key_type` is incorrectly identified as `'string'` in all test cases. This leads to inappropriate branch selections within the function, causing incorrect results.

To fix this bug, we need to update the logic for determining the `key_type` based on the actual type of the `key` parameter. We should handle the different types of `key` properly to ensure correct branching within the function.

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

    elif not is_list_like(key):
        return self.loc[key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        if isinstance(key, (list, np.ndarray, ExtensionArray, Series)):
            key_type = 'list_like'
        else:
            key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if key_type == 'list_like':
        return self.loc[key]

    return self.reindex(key)
```

In this corrected version, the key type is determined appropriately based on the actual type of the `key` parameter. This should resolve the bug and provide correct results for different scenarios.