## Bug Explanation
The bug in the `_get_with` function is caused by the incorrect handling of the `key` parameter when it is not a list-like type. The function assumes that if the `key` is not list-like, it should be passed to `self.loc[key]`. However, when the `key` is a scalar value or not recognized as a list-like type, it should be passed to `self.loc[key]`.

## Fix Strategy
To fix the bug, we need to correctly handle the case when `key` is a scalar or not a list-like type. We should check if the `key` is a scalar value or not recognized as list-like before calling `self.loc[key]`.

## The corrected version of the _get_with function

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        #  or label-based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    elif is_scalar(key) or not is_list_like(key):
        return self.loc[key]
    
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

With this corrected version of the `_get_with` function, the bug should be fixed, and the function should handle scalar values and non-list-like types correctly.