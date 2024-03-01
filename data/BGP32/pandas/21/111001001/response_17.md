The bug in the `_get_with` function arises from incorrectly inferring the `key_type` as `'string'` in all cases, leading to the wrong behavior of the function. This is due to the logic used to infer the dtype of the `key` parameter.

To fix the bug, we need to correctly infer the dtype of the `key` parameter and handle each type accordingly.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    # Check if key is a slice
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    # Check if key is a DataFrame
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    
    # Check if key is a tuple
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    # Check if key is not list-like
    elif not is_list_like(key):
        return self.loc[key]
    
    # Check if key is an iterable
    elif isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if not isinstance(key, (list, np.ndarray, ExtensionArray)):
            key = list(key)
    
        key_type = lib.infer_dtype(key)
    
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
    
        if isinstance(key, list):
            return self.loc[key]
    
        return self.reindex(key)
```

By correctly inferring the dtype of the `key` parameter based on its actual type, the `_get_with` function should now behave as expected with various input types.