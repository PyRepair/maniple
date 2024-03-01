### Bug Explanation
The bug in the `_get_with` function arises due to the incorrect handling of the `key` parameter. The function checks if the `key` is an instance of a list-like object, but when multiple conditions are stacked, it does not consider the case where `key` is a single scalar value (e.g., string).

### Bug Fix
To fix the bug, we need to update the logic to correctly handle the case when `key` is a scalar value. We can do this by first checking if `key` is a scalar and then returning the value from `.loc` method directly.

### Corrected Version
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if is_scalar(key):  # Check if key is a scalar (e.g., string)
        return self.loc[key]

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

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

This corrected version of the function now properly handles the scenario when the `key` parameter is a scalar value.