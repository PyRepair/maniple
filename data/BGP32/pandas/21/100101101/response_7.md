### Bug Explanation
The issue in the `_get_with` function arises from the incorrect handling of the key types when the input key is an ndarray or an Index object. The function wrongly infers the key type as `'string'` regardless of the actual type of the key, leading to unexpected behavior during indexing.

### Bug Fix Strategy
To fix this bug, we need to adjust the key type inference logic to correctly identify the key type when the input key is an ndarray or an Index object.

### Corrected Version of the Function
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

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

With this corrected version, the `_get_with` function should now correctly handle the key type inference for ndarrays and Index objects, ensuring that the function behaves as expected in the failing tests.