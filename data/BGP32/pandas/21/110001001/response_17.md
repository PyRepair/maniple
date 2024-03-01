The bug in the `_get_with` function seems to occur due to incorrect handling of the `key` parameter of different types. The function is intended to handle various types of input keys and return corresponding values. However, the logic for determining the `key_type` based on the input key is flawed.

The key issue arises from the inconsistency in handling different types of keys. In the provided cases, the key is incorrectly identified as `'string'` regardless of its actual type. This leads to incorrect branching in the subsequent logic, causing unexpected behavior.

To fix this bug, we need to ensure that the `key_type` is correctly determined based on the type of the `key` parameter. We can modify the logic to infer the `key_type` accurately for each type of key. Additionally, we need to handle the different key types appropriately to return the expected values.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError("Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column")
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    elif is_scalar(key):
        return self.loc[key]
    
    elif isinstance(key, Index):
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

This corrected version includes a check for scalar keys using `is_scalar()` and adjusts the logic for accurately determining the `key_type`. By addressing these issues, the function should now handle different types of keys appropriately and return the expected values based on the input key type.