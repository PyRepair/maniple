### Analysis
The `_get_with` function in the `Series` class is trying to handle different types of input `key` objects to return the corresponding values. However, there are some issues in the implementation that are causing the function to fail in the test cases.

1. The function is not appropriately handling the case when the `key` is a list, ndarray, Index, or Series. It should be able to index the `Series` object with these types of inputs, but it fails due to a KeyError.
2. The function is incorrectly inferring the `key_type` as "integer" instead of "string" when dealing with a string input which leads to an incorrect indexing method being used.

### Bug Fix Strategy
1. Adjust the function implementation to correctly handle list, ndarray, Index, and Series types of `key` inputs to properly index the `Series` object in those cases.
2. Update the logic to correctly infer the `key_type` based on the type of input `key` to select the appropriate indexing method (loc or iloc) for the `Series`.

### Corrected Function
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
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)
        
        if key_type == "string":
            return self.loc[key]
        else:
            return self.iloc[key]
    
    return self.reindex(key)
```

By making these modifications to the `_get_with` function, it should now correctly handle the different types of `key` inputs and return the appropriate values from the `Series` object.