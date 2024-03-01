The bug in the `_get_with` function is caused by the incorrect handling of the key type when it is not recognized as a list-like object. In the given cases, the key type is identified as `'string'`, which leads to the incorrect if condition execution and trying to access the `loc` attribute of the key variable.

To fix this bug, we should update the condition checking for non-list-like keys to correctly differentiate between different key types.

Here is the corrected version of the `_get_with` function:

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

    if not is_list_like(key) and not isinstance(key, Index):
        key = [key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == 'integer':
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version ensures that non-list-like keys are appropriately handled and prevents the incorrect access to `loc` for keys that are not supposed to be treated as lists.