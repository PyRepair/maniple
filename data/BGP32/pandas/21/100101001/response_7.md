### Bug Analysis:
The bug in the `_get_with` function lies in the handling of the key parameter. The function incorrectly identifies the key type as `'string'` regardless of the actual type of the key, causing the function to always return the wrong result. This leads to failing tests because the function cannot handle different types of keys correctly.

### Bug Fix Strategy:
To fix the bug, we need to correctly determine the type of the key parameter and handle each type appropriately. We should update the logic to handle different key types like list, ndarray, Index, Series, etc., based on their actual types.

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

    elif not is_list_like(key) or isinstance(key, Series):
        try:
            key = ensure_index(key)
        except (ValueError, TypeError):
            raise KeyError(f"{key!r} not in index")

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray)):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version of the function correctly handles different types of keys and ensures that the function returns the expected results for each type. It also includes error handling to raise a KeyError when the key is invalid.