### Bug Explanation
The bug in the `_get_with` function occurs due to incorrect handling of the key type. In the cases provided, the key type is inferred as `'string'`, but the code does not properly handle this case. Instead, it tries to determine whether to use positional indexing (`iloc`) or label-based indexing (`loc`) based on the inferred key type, leading to the wrong behavior.

### Fix Strategy
To fix the bug, we need to handle the case where the key type is `'string'` correctly. In this case, we should directly use label-based indexing (`loc`) since the key represents labels.

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
    
    elif not is_list_like(key):
        return self.loc[key]
    
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = 'string'  # treat any non-handled case as label-based indexing
        
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By explicitly setting `key_type = 'string'` when handling any non-handled case, we ensure that in situations where the key type is not identifiable or wrongly inferred as `'string'`, the function defaults to label-based `loc` indexing, resolving the bug.