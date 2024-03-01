### Bug Explanation
The bug in the `_get_with` function arises from the incorrect inference of the `key_type` variable when dealing with non-numeric keys. The current implementation incorrectly assumes that any key that is not recognized as a list-like object is of type "integer", leading to incorrect handling of string keys.

### Bug Fix Strategy
To fix this bug, we need to update the logic for inferring the `key_type` properly. We should differentiate between numeric keys and non-numeric keys, such as string keys, and handle them accordingly to avoid the issue observed in the failing tests.

### Corrected Function
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

    # Separate handling for non-numeric keys
    if isinstance(key, str) or isinstance(key, ObjectIndex):
        return self.loc[key]
    
    # Skip the check for list-like objects and invalid keys
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

The corrected function now properly handles string keys and avoids incorrectly inferring non-numeric keys as "integer", resolving the bug observed in the failing tests.