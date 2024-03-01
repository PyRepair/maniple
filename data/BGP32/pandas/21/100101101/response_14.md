The bug in the `_get_with` function lies in the comparison of the `key_type` variable with the string `'integer'`. The key_type is incorrectly assigned as `'string'` in all cases, leading to the incorrect behavior of the function when dealing with different types of keys.

To fix this bug, we need to correctly infer the dtype of the key and compare it with the correct type for handling integer keys.

Here's the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError("Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column")
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type in ['integer', 'int']:
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version properly infers the dtype of the key and compares it with `'integer'` or `'int'` to handle integer keys correctly. This fix should address the bug and make the function behave as expected in the failing test cases.