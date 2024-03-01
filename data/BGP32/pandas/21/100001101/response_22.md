### Bug Explanation
The bug in the `_get_with` function arises from incorrectly determining the `key_type` when handling various types of input `key` values. The code fails to correctly infer the type when the key is a list containing a string or when using indexing from a Series object.

### Bug Fix Strategy
To fix the bug, we need to ensure that the `key_type` is correctly identified based on the type of the `key` input. This involves properly handling the cases where `key` is a list or a Series object. Additionally, the code should account for different types of keys and properly reindex the Series based on the key type.

### Corrected Code
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

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if is_list_like(key) and all(is_scalar(x) for x in key):
        return self.loc[key]

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray, Series)):
        key = np.asarray(key)

    if isinstance(key, np.ndarray) and key.dtype.kind in 'biufcmM':
        key = ensure_index(key)

    return self.reindex(key)
```

By making these changes, the corrected function should handle the various input types correctly and infer the `key_type` accordingly. This revised code should address the bug and align the function's behavior with the expected input/output values.