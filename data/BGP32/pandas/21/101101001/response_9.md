### Bug Analysis:
The bug occurs in the `_get_with` function where the key is not being handled correctly in all cases. The bug causes an issue when the key is a list or ndarray where the inferred type is being incorrectly set to `'string'`, leading to incorrect behavior and failing tests.

### Bug Cause:
The bug is caused by the incorrect handling of the key type when it is a list or ndarray. The function wrongly infers the key type as `'string'`, which then leads to incorrect indexing behavior.

### Bug Fix:
To fix the bug, we need to ensure that when the key is a list or ndarray, it is appropriately handled without incorrectly inferring the key type as `'string'`.

### Corrected Version of the Function:
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

    if isinstance(key, Index):
        key_type = key.inferred_type
    elif isinstance(key, list) or isinstance(key, np.ndarray):
        key_type = lib.infer_dtype(key, skipna=False)
    else:
        key_type = lib.infer_dtype([key], skipna=False)[0]

    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        #  (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

By updating the key_type assignment for lists and ndarrays and ensuring proper handling of keys, the corrected function should now correctly handle the provided failing tests.