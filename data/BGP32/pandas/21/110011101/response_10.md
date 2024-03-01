### Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the key types, specifically when the key is passed as a Series. The function incorrectly infers the key type as "string" when it should take into account the actual type of the key passed.

### Solution Strategy
To fix the bug, we need to ensure that the key type is correctly identified based on the type of key passed as an input parameter. We should handle different key types appropriately to avoid the KeyError issue encountered during the test.

### Corrected Version of the Function
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

    if is_list_like(key) and not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if is_scalar(key):
            return self.loc[key]
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

By updating the conditional checks and handling different key types appropriately, we ensure that the `_get_with` function behaves correctly for various key inputs.