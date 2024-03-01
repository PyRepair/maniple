### Bug Analysis
The bug occurs in the `_get_with` function of the `Series` class. The function is intended to handle different types of keys for indexing a Series. However, the issue arises when the key is not list-like and is a single scalar value, consequently leading to a KeyError when attempting to access the Series element.

### Bug Explanation
1. In the failing test scenarios, the keys used for indexing are of type `list`, `ndarray`, `Index`, and `Series`. 
2. In the `_get_with` function, when the key is not list-like, it reaches the condition `elif not is_list_like(key)`, which accesses the `self.loc[key]`, assuming `key` is a valid index. This causes an issue when `key` is a scalar value, leading to a KeyError.

### Bug Fix
To fix the bug, we need to handle the case when the key is not list-like and is a scalar value properly. We can modify the condition to check if `key` is a scalar and then directly return the value from `self.loc`. 

Here's the corrected version of the `_get_with` function:

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
    
    elif is_scalar(key):
        return self.loc[key]
    
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

The added condition `elif is_scalar(key)` ensures that if `key` is a scalar value, it is directly accessed using `self.loc[key]`. This prevents the KeyError from occurring when indexing with a single scalar value.