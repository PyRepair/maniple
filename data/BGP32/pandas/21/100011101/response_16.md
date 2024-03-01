### Bug Explanation:
The bug in the `_get_with` function arises from the incorrect handling of the key parameter when it is a list or array of values that do not match any index in the Series. The function incorrectly assigns the key type as `'string'`, which is causing the KeyError to not be raised in the failing test cases.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the correct key type is identified and handled properly when the key does not match any index in the Series. We can update the logic to check if the key is in the Series index before proceeding with further operations.

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

    elif not is_list_like(key):
        return self.loc[key]

    if not is_scalar(key):
        if not any(key in self.index):
            raise KeyError(f"None of {key} are in the index")
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By updating the function to correctly check if the key is in the Series index before proceeding, we ensure that a KeyError is raised if the key does not match any index values. This fix should address the issues observed in the failing test cases.