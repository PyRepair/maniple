The bug in the `_get_with` function arises from the incorrect handling of the input `key` parameter. The function is not properly detecting the type of `key`, leading to errors in the subsequent logic of the function. 

To fix the bug, we need to ensure that the type of `key` is correctly identified and processed accordingly. In the provided cases, the expected behavior is to determine the type of `key` (list, ndarray, Index, Series) and then take the appropriate actions based on that type.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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
      
    elif isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
  
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
        
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    elif not is_list_like(key):
        return self.loc[key]
    
    else:
        raise TypeError("Unsupported type for key: {}".format(type(key)))
```

By correctly identifying the type of `key` and processing it accordingly, this fixed version of the `_get_with` function should now pass the failing test cases and provide the expected output values.