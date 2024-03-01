### Bug Explanation:
The bug occurs in the `_get_with` function when it tries to determine the `key_type` based on the input `key`. In the cases provided, the `key_type` is incorrectly set to `'string'` when it should be `'object'` or another type based on the input `key`.

### Bug Fix:
To fix the bug, we need to correctly infer the `key_type` based on the type of the `key` input parameter. We should also handle different types of `key` inputs appropriately to determine the `key_type` accurately.

### Corrected Function:
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

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    # Handle the case when key_type is 'mixed' (e.g., when key input is a Series)
    if key_type == 'mixed':
        key_type = lib.infer_dtype(key.tolist())

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By using the corrected version of the `_get_with` function, the bug should be resolved, and the function should now correctly determine the `key_type` based on the input `key` parameters, passing the failing test cases.