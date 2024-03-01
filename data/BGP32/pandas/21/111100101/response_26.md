## Bug Explanation
The bug in the `_get_with` function lies in the condition where `key_type` is determined. The bug is caused by the incorrect branching of logic when handling different types of input keys. The code mistakenly treats keys of type `'string'` as `'integer'`, leading to the wrong indexing method being selected. This results in a KeyError when looking up a key that is not present in the Series index.

## Bug Fix Strategy
To fix the bug, we need to correctly identify the type of key being provided and choose the appropriate indexing method based on the type. We should handle different types of keys, such as scalar, list, ndarray, and Index, separately to ensure proper indexing.

## Corrected Code
```python
def _get_with(self, key):
    # , slice, fancy integer or otherwise
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

    if is_scalar(key):
        try:
            return self.loc[key]
        except KeyError:
            pass

    key_arr = np.asarray(key)

    if is_bool(key_arr):
        return self.loc[key]
    elif is_categorical_dtype(key_arr.dtype):
        return self.loc[key]
    elif is_object_dtype(key_arr.dtype):
        return self.loc[key]

    if is_integer(key):
        if isinstance(key, (list, np.ndarray, Series, Index)) or is_extension_array_dtype(key):
            if isinstance(key, Index):
                key_type = key.inferred_type
            else:
                key_type = lib.infer_dtype(key, skipna=False)
            
            if key_type == "integer":
                if not self.index._should_fallback_to_positional():
                    return self.loc[key]
                else:
                    return self.iloc[key]

    return self.reindex(key)
```

With the corrected code above, the `_get_with` function should handle various key types correctly and return the expected values for the failing test cases provided. Make sure to test the corrected code with the failing test to verify its functionality.