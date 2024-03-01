The bug in the `_get_with` function arises from the incorrect handling of the `key` parameter. The function is not properly distinguishing between different types of keys, resulting in an incorrect value for `key_type`.

To fix the bug, we need to update the logic for determining the type of `key` and handle each case appropriately. Here is the corrected version of the `_get_with` function:

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
        if is_integer(key):
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        else:
            return self.loc[key]

    elif isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        
        return self.loc[key]
    
    return self.reindex(key)
```

In this corrected version, we have added a check for scalars using the `is_scalar` function and distinguished between integer keys and other types of keys. This should address the issue of incorrectly inferring the `key_type` and handle the key variable appropriately based on its type.