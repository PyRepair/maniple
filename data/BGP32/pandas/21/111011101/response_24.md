The bug in the `_get_with` function arises from the incorrect handling of the input key types. The function should be able to handle different types of keys, such as lists, numpy arrays, Series, and Index. The function incorrectly infers the key type as "integer" for keys that are actually strings or objects, leading to the KeyError in the failing tests.

To fix the bug, we need to adjust the logic for determining the key type and appropriately select the indexing method (loc or iloc) based on the key type.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError("Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column")
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    if is_list_like(key) and not isinstance(key, (np.ndarray, Index)):
        key = list(key)
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type in ["integer", "string"]:
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    return self.reindex(key)
```

This corrected version should now properly handle different key types like lists, numpy arrays, Series, and Index, selecting the appropriate indexing method (loc or iloc) based on the key type. This should resolve the KeyError issues in the failing tests.