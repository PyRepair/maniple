### Bug Explanation:
The bug in the `_get_with` function arises from the incorrect handling of the key type when it is not recognized as a list-like object. The function mistakenly assumes that the key is a scalar and tries to access it using `self.loc[key]`. This leads to a KeyError when attempting to index the Series with a key that does not match any values in the index.

### Bug Fix Strategy:
To fix the bug, we need to update the logic for handling non-list-like keys to prevent KeyError when accessing the Series. We should ensure that the key type is correctly identified and handled based on its type.

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

    # Handling non-list-like keys
    if not is_list_like(key):
        if is_scalar(key):
            key = [key]
        else:
            key = [key]
    
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

By modifying the logic to check for scalar keys and convert them into a list, we ensure that the Series can be indexed correctly without raising KeyError for non-matching keys.This corrected version should pass the failing test cases and provide the expected output for different key types.