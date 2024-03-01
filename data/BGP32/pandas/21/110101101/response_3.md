### Bug Explanation
The bug in the `_get_with` function occurs because it incorrectly identifies the `key_type` when the key is not list-like. In the failing tests, when `key` is not list-like, the function tries to access `key` directly with `self.loc[key]`. However, the function incorrectly infers `key_type` as `'string'` instead of `'object'`, leading to a KeyError when trying to access a non-existent key in the index.

### Bug Fix Strategy
To fix the bug, we need to correctly infer the `key_type` based on the input `key` when it is not list-like. We can achieve this by checking the type of the key and modifying the inference logic accordingly.

### Corrected Version
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

    if is_scalar(key) or isinstance(key, ABCSeries):
        return self.loc[key]

    if not is_list_like(key):
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

By adding the `is_scalar` check and properly handling non-list-like keys as scalars for direct indexing using `self.loc[key]`, we can fix the bug and ensure that the corrected function passes the failing tests.