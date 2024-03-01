### Bug Explanation
The bug in the `_get_with` function is caused by the incorrect handling of the key_type when it is identified as "string" in the code. The bug leads to the wrong execution path being chosen for indexing, which results in a Key Error when trying to access the key value.

### Bug Fix Strategy
To fix the bug, we need to correctly handle the case where the key_type is identified as "string". We should ensure that the key is treated as a label-based index for the loc accessor. Additionally, we need to update the key_type identification logic to account for different types correctly.

### Corrected Code
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determin if this slice is positional
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

    elif not is_list_like(key):
        # e.g. scalars that aren't recognized by lib.is_scalar, GH#32684
        return self.loc[key]

    # Correcting key_type identification logic
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        #  (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        # added specific handling for 'string' key_type
        if key_type == "string":
            return self.loc[key]
        
        return self.reindex(key)

    # handle the dup indexing case GH#4246
    return self.loc[key]
```

With this correction, the `_get_with` function should now correctly handle the key types and choose the appropriate indexing method. This fix should make the function pass the failing test cases provided.