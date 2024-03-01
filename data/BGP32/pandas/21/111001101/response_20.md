## Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the key types. The function is supposed to handle different types of keys to retrieve values from the Series. However, the logic for determining the `key_type` is flawed, leading to incorrect branching decisions. The bug causes the function to return the wrong values for certain input types, such as strings.

## Bug Fix Strategy
To fix the bug in the `_get_with` function, we need to properly identify the type of the key and adjust the branching logic accordingly. We should ensure that the function correctly handles different key types and retrieves the values appropriately.

## The corrected version of the _get_with function

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    if isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    
    if isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    if is_scalar(key):
        return self.loc[key]
    
    if not is_list_like(key):
        raise KeyError("Invalid key type")
    
    if isinstance(key, (Index, np.ndarray, ExtensionArray, Series)):
        return self.loc[key]
    
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

This revised function properly handles the key types and provides accurate branches based on the type of keys passed to it. The correction ensures that the function returns the correct values for different input types, resolving the bug.