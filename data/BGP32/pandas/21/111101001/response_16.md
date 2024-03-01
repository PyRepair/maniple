The bug in the `_get_with` function arises from the incorrect handling of the key type when it is a list or array containing scalar values that are not recognized as scalar by `lib.is_scalar` function. This leads to a mistaken inference of the key type as `'string'` instead of `'object'`.

To fix this bug, we need to update the key type check for non-list-like keys to correctly identify scalar values that are not recognized by `lib.is_scalar` as 'object' type instead of 'string'.

Here is the corrected version of the `_get_with` function:

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

    if not is_list_like(key):
        # Corrected key type handling for non-list-like keys
        key = [key]
    
    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

By updating the key handling for non-list-like keys, the corrected function should now correctly identify the key type as `'object'` in cases where scalar values are not recognized as scalar by `lib.is_scalar`. This correction should resolve the issue with the failing tests.