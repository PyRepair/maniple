### Bug Explanation
The bug in the `_get_with` function arises from the logic to determine the `key_type`. The issue occurs because even if the `key` variable is a list or array of strings, the `key_type` is inferred as `'integer'`, leading to incorrect handling of the key in subsequent steps.

### Bug Fix Strategy
To fix the bug, we need to update the logic for inferring the `key_type` based on the type of the `key` variable. If the `key` is a list or array of strings, the `key_type` should be set to `'string'`. This will ensure that the correct indexing method is used for the subsequent operations.

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

    # Update the logic for inferring key_type correctly
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

With this corrected code, the function should now correctly infer the `key_type` based on the type of `key`, ensuring proper indexing behavior for string keys.