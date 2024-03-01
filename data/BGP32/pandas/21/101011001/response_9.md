### Bug Analysis:
- The bug occurs when the function `_get_with` encounters a key that is a single-element array, an Index, or a Series as the input.
- In each case, the function incorrectly infers the `key_type` as `'string'`, which leads to the wrong logic path being taken, resulting in the KeyError when trying to index the Series.
- The function should handle these cases differently to correctly index the Series based on the type of the key.

### Bug Fix Strategy:
- We need to update the logic for handling different types of keys to correctly index the Series.
- By checking the type of the key properly, we can ensure that the correct indexing method (`loc` or `iloc`) is used based on the key type.

### Corrected Version of the Function:
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

    elif is_scalar(key):
        return self.loc[key]

    elif isinstance(key, (list, np.ndarray, ExtensionArray, Series)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        
        elif key_type == "string":
            return self.loc[key]
    
    return self.reindex(key)
```

By making these changes, the corrected function should now be able to correctly handle different types of keys and avoid the KeyError that was occurring in the failing tests.