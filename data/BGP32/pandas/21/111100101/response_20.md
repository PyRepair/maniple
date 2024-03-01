The bug in the `_get_with` function arises from the incorrect handling of the key type when it is not a list-like object. The function is not accurately determining the key_type based on the input key and is not handling the case where the key_type is a string.

To fix the bug, we need to correctly infer the key_type when the key is not a list-like object and appropriately handle the case where the key_type is a string.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif not is_list_like(key):
        key = [key]  # Wrap the scalar key in a list
    
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        # Check if key is a supported type for indexing
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)
        
        if key_type == "string":
            return self.loc[key]
        elif key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        else:
            return self.reindex(key)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
```

With this correction, the function will correctly handle the key type when it is not a list-like object and ensure that the appropriate indexing operation is performed based on the key_type inferred. This corrected version should pass the failing test cases provided.