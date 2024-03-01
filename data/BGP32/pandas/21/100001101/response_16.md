### Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the case where `key` is of type 'string'. The function wrongly infers the `key_type` as 'integer' instead of 'string' and tries to treat it as an integer indexer. This leads to an error since the key is actually a 'string'.

### Bug Fix Strategy
To fix the bug, we need to correctly identify the type of the `key` parameter and handle the 'string' type case appropriately. We can modify the implementation to correctly handle 'string' type keys and make sure it does not try to treat them as integer indexes.

### Corrected Implementation
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
    elif not is_list_like(key):
        return self.loc[key]

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
    elif key_type == "string":
        return self.loc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By adding a specific check for the 'string' type and correctly handling it by using `self.loc[key]`, we ensure that the function can handle 'string' keys appropriately without trying to treat them as integer indexes.