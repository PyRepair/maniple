The bug in the `_get_with` function arises from the handling of different types of indexers. When the indexer is a list-like object, it is not properly handled, leading to a KeyError in certain cases.

Based on the runtime values and types of variables in the failing tests, the issue stems from the incorrect handling of list-like indexers such as a plain list or ndarray.

To fix the bug, we should update the handling of list-like indexers in the `_get_with` function to ensure consistent behavior for all types of indexers.

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
    
    elif is_list_like(key) and not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)
    
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

This updated version includes proper handling for list-like indexers, ensuring consistent behavior for all cases.

After applying this fix, the `_get_with` function should pass the failing tests and resolve the issue reported on GitHub.