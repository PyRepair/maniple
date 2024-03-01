The bug in the `_get_with` function arises due to the incorrect evaluation of the key type, leading to the wrong path being taken in the code logic. The issue is primarily related to the incorrect handling of the key type in different scenarios.

### Bug Explanation:
1. In the provided cases, the key is expected to be a list, ndarray, or Index, but the function fails to correctly identify the key type.
2. The function incorrectly identifies the key as a 'string' in all cases, leading to the wrong path being taken for processing the key.

### Fix Strategy:
1. Update the code logic to accurately determine the key type based on the input key variable to ensure correct processing.
2. Implement proper checks to handle different key types such as list, ndarray, Index, etc., and adjust the code flow accordingly.

### Corrected Version of the `_get_with` Function:
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
    
    if not is_list_like(key):
        return self.loc[key]
    
    if isinstance(key, (np.ndarray, Series)):
        return self.loc[key]
    
    if isinstance(key, Index):
        key_type = key.inferred_type
        key = key.values
    else:
        key_type = lib.infer_dtype(key)
        
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By incorporating these changes, the corrected function should be able to accurately determine the key type and handle different scenarios effectively.