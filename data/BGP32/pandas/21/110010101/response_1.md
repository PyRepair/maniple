### Analysis
The `_get_with` function in the `Series` class is supposed to handle different types of input keys and return the corresponding values. However, there are multiple issues with the current implementation:
1. The function does not handle the case when `key` is an ndarray or Index properly.
2. The function incorrectly assigns the variable `key_type` based on the type of `key`, leading to unexpected results.
3. The function may not correctly handle scalar values that are not recognized as list-like.

### Bug Explanation
The bug occurs because the function fails to correctly identify the type of `key` when it is an ndarray or Index. This leads to the incorrect inference of the `key_type`, causing the function to return unexpected results.

### Bug Fix Strategy
To fix the bug, we need to update the function to properly handle ndarray and Index types of `key`. We also need to ensure that the `key_type` is inferred correctly based on the type and content of `key`.

### Corrected Function
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError("Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column")
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    elif not is_list_like(key):
        return self.loc[key]
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "string":
        return self.loc[key]
    elif key_type == "integer" and self.index._should_fallback_to_positional():
        return self.iloc[key]
    
    if isinstance(key, list):
        return self.loc[key]
    
    return self.reindex(key)
```

By updating the function as shown above, we address the issues related to handling different types of keys and correctly inferring the `key_type` for further processing. This corrected version should now pass the failing test cases and satisfy the expected input/output values.