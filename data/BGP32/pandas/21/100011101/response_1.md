### Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the `key_type` variable. The function incorrectly determines the `key_type` as `'string'` in all cases, which leads to incorrect indexing actions based on this incorrect type assumption. This incorrect type handling causes the function to not raise a `KeyError` as expected in the failing tests.

### Bug Fix Strategy
To fix the bug, we need to properly infer the type of the `key` parameter and handle it accordingly. This involves accurately determining whether the key corresponds to an integer, a list, a slice, etc., and choosing the appropriate indexing approach based on this type inference.

### Corrected Version of the Function
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
    
    elif is_scalar(key):
        return self.loc[key]
    
    elif is_list_like(key):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)
        
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        
        elif key_type == "boolean":
            if not com.is_bool_indexer(key):
                raise KeyError("Boolean indexing is not supported")
            return self.loc[key]
        
        elif key_type == "string":
            return self.loc[key]
    
    return self.reindex(key)
```

The corrected version introduces proper type inference for the `key` parameter and handles indexing based on the inferred type. This approach ensures that the correct indexing method is used depending on the type of the key, resolving the bug that caused the failing tests.