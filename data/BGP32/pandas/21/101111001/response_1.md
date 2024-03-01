The bug in the `_get_with` function is caused by incorrectly inferring the `key_type` as `'string'` for all input cases, regardless of the actual type of the `key`.

To fix the bug, we need to properly determine the type of the `key` and adjust the behavior accordingly.

Here is the corrected version of the `_get_with` function:

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

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        inferred_type = lib.infer_dtype(key, skipna=False)
    elif isinstance(key, Index):
        inferred_type = key.inferred_type
    else:
        raise TypeError(f"Unsupported key type: {type(key)}")

    if inferred_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

With this correction, the function should properly infer the type of the `key` and choose the appropriate path depending on the type. This fix should resolve the failing tests.