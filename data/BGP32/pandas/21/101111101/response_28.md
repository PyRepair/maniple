The bug in the `_get_with()` function arises from the incorrect handling of non-list-like keys. The function should not directly try to access the key through `self.loc[key]` if the key is not list-like. Instead, it should check if the key is an instance of `Index` before inferring the key type and deciding between positional or label-based indexing.

Here is the corrected version of the `_get_with()` function:

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

This corrected version ensures that the key type is correctly inferred, and the appropriate indexing method (`.loc` or `.iloc`) is chosen based on the key type. This fix should address the failing tests and align with the expected input/output values.