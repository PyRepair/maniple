The bug in the `_get_with` function arises from the handling of the `key_type` variable when the `key` input parameter is not recognized as a valid index type. The issue is that the variable `key_type` is incorrectly identified as `'integer'` in many scenarios, leading to the wrong return path being taken.

To fix the bug, we should adjust the logic related to determining the type of the `key` input parameter so that it correctly identifies the type as `'string'` when applicable.

Here is the corrected version of the `_get_with` function:

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

    elif is_scalar(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = lib.infer_dtype(key, skipna=False)
        
        if key_type == "string":
            return self.loc[key]
        
        # For any other type of key, fall back to reindex
        return self.reindex(key)
    
    # Handling duplicate indexing case GH#4246
    return self.loc[key]
```

Applying this correction should resolve the issue and make the function behave as expected, passing the failing test cases provided.