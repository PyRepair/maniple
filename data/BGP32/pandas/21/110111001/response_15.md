The bug in the `_get_with` function lies in the incorrect handling of the `key_type` variable and the subsequent decision-making based on the type of `key_type`. The function incorrectly infers the `key_type` as `'string'` for all input cases, causing the function to always return `self.loc[key]` regardless of the actual type of `key`.

To fix this bug, we need to properly infer the type of `key` and handle each case accordingly. We can update the `_get_with` function to correctly determine the type of `key` and choose the appropriate indexing method (`iloc` or `loc`) based on the type. Below is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    if isinstance(key, ABCDataFrame):
        raise TypeError("Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column")
    
    if isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    if not is_list_like(key):
        return self.loc[key]
    
    # Handle list, ndarray, Index, Series
    if isinstance(key, (list, np.ndarray, Index, Series)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)
       
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
    
    # Handle other cases like non-conventional scalars
    return self.loc[key]
```

By making these changes, the `_get_with` function should now correctly infer the type of `key` and choose the appropriate indexing method (`iloc` or `loc`) based on that type.

This corrected version should address the bug and pass the failing tests.