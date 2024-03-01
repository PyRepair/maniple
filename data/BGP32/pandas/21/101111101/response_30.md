The bug in the `_get_with` function occurs because the key_type is incorrectly identified as "string" instead of "object" when the key is a list-like object like an array or Index. This leads to the function incorrectly trying to access the key using `self.reindex(key)` instead of `self.loc[key]`, causing a KeyError.

To fix this bug, we need to correctly identify the key_type when the key is a list-like object. We can achieve this by updating the logic to appropriately handle list-like keys.

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
    
    # Updated logic for handling list-like keys
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

This corrected version ensures that the key_type is correctly identified for list-like keys, preventing the KeyError. The function should now pass the failing tests with the expected input/output values.