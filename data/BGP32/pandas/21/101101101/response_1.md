### Bug Explanation:
The bug occurs when the `key_type` is determined as `'string'` regardless of the type of key provided to the `_get_with` function. This issue leads to incorrect behavior in handling different types of keys, resulting in failing tests where the expectation is for the function to handle the keys appropriately based on their types.

### Fix Strategy:
To fix the bug, we need to correctly determine the type of the `key` parameter and handle each type accordingly. We should ensure that the behavior is consistent with the expected input types and outcomes based on the test cases provided.

### Corrected Function:
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    if isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    
    if isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    if is_scalar(key):
        return self.loc[key]
    
    # Check if key is a list-like object or if it needs to be converted to a list
    if not is_list_like(key):
        key = [key]
        
    # Determine the type of the key
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

By updating the `_get_with` function as provided above, the function should now correctly handle different types of keys, matching the expected behavior for the failing test cases.