### Bug Explanation:
The bug in the `_get_with` function arises from the incorrect handling of the key type when the key is a list or ndarray. The function incorrectly infers the key type as "integer" regardless of the actual data type in the key. This leads to the wrong decision on whether to use positional indexing (`iloc`) or label-based indexing (`loc`), resulting in a KeyError when trying to access a non-existent index.

### Bug Fix Strategy:
To fix the bug, we need to accurately determine the key type when the key is a list or ndarray. By properly identifying the key type, we can decide whether to use label-based or positional indexing to access the data.

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

    # Check if the key is list-like
    if not is_list_like(key):
        return self.loc[key]

    key = ensure_index(key)

    # Infer the proper data type of the key
    key_type = lib.infer_dtype(key, skipna=False)

    # Handle integer index type scenario
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, Index):
        key = key.tolist()

    if key_type == "object":
        try:
            key = key.astype('object')
        except (ValueError, TypeError):
            pass
    
    return self.reindex(key)
```

By updating the `_get_with` function with the corrected version above, the bug should be fixed, and the failing test cases should pass without raising a KeyError.