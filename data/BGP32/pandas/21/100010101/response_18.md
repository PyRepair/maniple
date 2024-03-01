### Bug Analysis
1. The function `_get_with` is intended to handle different types of keys for indexing a Series.
2. The bug seems to be in the handling of the key types and the logic to decide whether to use positional indexing (`iloc`) or label-based indexing (`loc`).
3. The error messages indicate that the function is not properly handling the keys passed as different types (list, ndarray, Index, Series) in the failing test cases.
4. The key_type variable seems to always result in 'string' instead of 'integer', which may be causing the function to incorrectly try to use label-based indexing.
5. The function is not properly distinguishing between key types and applying the correct indexing method.

### Bug Fix Strategy
To fix the bug in the function `_get_with`, we need to:
1. Ensure correct identification of key types.
2. Use the appropriate indexing method (`iloc` or `loc`) based on the key type.
3. Treat each key type differently to ensure the correct behavior for different input types.

### Corrected Version
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

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = lib.infer_dtype(key, skipna=False)
    else:
        raise TypeError("Unsupported type for index key")

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, Index):
        key_type = key.inferred_type

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

With the corrected logic in place, the function should now properly handle different key types and apply the correct indexing method based on the type of key provided.