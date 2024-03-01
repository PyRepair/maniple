### Bug Explanation
The bug in the `_get_with` function occurs because the type checking logic for `key` is flawed. It assumes that if `key` is not a list-like object, then it must be treated as a scalar and tries to access it using `self.loc[key]`. However, in several cases where `key` is not a list-like object, but still a valid index/key (like a string in this case), accessing `self.loc[key]` will raise a `KeyError`.

### Bug Fix Strategy
To fix the bug, we need to modify the logic for handling non-list-like keys. Instead of directly accessing `self.loc[key]`, we should first check if the key exists in `self.index` before using `loc` or `iloc` to retrieve the corresponding value.

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

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]
    elif self.index.isin([key]).any():
        return self.loc[key]

    return self.reindex(key)
```

This corrected version of the `_get_with` function implements a check to verify if the key exists in the index before attempting to access it using `loc`. It ensures that non-list-like keys that are valid indices are correctly handled without raising errors.