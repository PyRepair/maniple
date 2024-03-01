The bug in the `_get_with` function stems from the incorrect handling of the key parameter, specifically when `key` is a list-like object such as a NumPy array, Index, or Series. The function fails to correctly index the Series object, leading to a KeyError in the failing tests.

To fix this bug, we need to ensure that when `key` is list-like, it is properly processed to retrieve the desired values from the Series object.

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
    
    if is_list_like(key):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)
    
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
    
        if isinstance(key, (list, np.ndarray, ExtensionArray, Series)):
            return self.loc[key]
    
    return self.reindex(key)
```

This corrected version checks if the `key` is list-like using the `is_list_like` function and then correctly uses `loc` to retrieve the values if it is list-like.

By making these changes, the `_get_with` function should now be able to handle list-like objects such as NumPy arrays, Index objects, and Series objects correctly, passing the failing tests and providing the expected output.