### Bug Explanation
The bug in the `_get_with` function arises from the logic for handling the `key` parameter. The function checks if `key` is not list-like and then attempts to access `self.loc[key]`. However, when `key` is an ndarray or an Index object, this operation leads to a KeyError because the key is not found in the index.

### Bug Fix Strategy
To fix the bug, we need to modify the logic for handling different types of `key`, especially when `key` is an ndarray or an Index object. We should ensure that the key is always present in the index before accessing it.

### Corrected Version of the Function
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

    elif not is_list_like(key) or isinstance(key, (np.ndarray, Index)):
        return self.reindex(key)

    key = list(key)
    key_type = lib.infer_dtype(key, skipna=False)

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

By making these changes, we ensure that the key is correctly handled for different types, preventing the KeyError issue encountered in the failing tests.