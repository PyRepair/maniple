### Bug Explanation
The bug occurs because the check for the key_type being "string" is misplaced in the `_get_with` function. The key_type is incorrectly inferred as "string", which leads to the wrong execution path in the function. The key_type should be correctly inferred based on the input key and then used to determine the appropriate action.

### Fix Strategy
1. Move the inference of key_type to the correct location after identifying the type of the key.
2. Use the correct key_type to decide whether to use positional indexing (iloc) or label-based indexing (loc).

### The corrected version of the function
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        #  or label based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    key = ensure_index(key)

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        #  (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type

        if key_type == "string":
            return self.loc[key]

        if isinstance(key, list) or isinstance(key, Index):
            # handle the dup indexing case GH#4246
            return self.loc[key]
    return self.reindex(key)
```

By moving the inference of `key_type` after identifying the type of `key` and using it correctly in decision making, the corrected function should pass the failing tests and exhibit the expected behavior in all cases.