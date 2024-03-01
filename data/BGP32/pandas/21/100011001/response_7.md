### Analysis
The buggy function `_get_with` is designed to handle different types of keys for indexing a Series. However, it fails to handle `Index` and `ndarray` keys correctly, as seen in the failing tests. The function incorrectly infers the `key_type` as `'integer'` or `'boolean'`, leading to the wrong indexing strategy.

### Bug Explanation
In the failing tests:
1. The function incorrectly infers the `key_type` as `'string'` instead of `'object'`.
2. Due to the incorrect `key_type` inference, the function chooses the wrong indexing strategy (`self.loc[key]` instead of `self.reindex(key)`).

### Bug Fix
To fix the bug, we should update the logic for inferring the `key_type` based on the type of key provided. If the key is an `Index` or `ndarray`, the function should accurately identify the `key_type` as `'object'` and then use the appropriate indexing strategy.

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

    elif not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index) or isinstance(key, np.ndarray):
        key_type = 'object'
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

By updating the `key_type` detection logic to correctly identify `'object'` for `Index` and `ndarray` keys, we address the bug in the function and ensure correct indexing for these types of keys.