The bug in the provided `_get_with` function lies in the handling of the key_type variable. The function is incorrectly assigning the `key_type` as `'integer'` when it should be `'string'` in the cases provided by the failing test. This is causing the function to incorrectly determine whether to use `iloc[key]` or `loc[key]` for indexing.

To fix this bug, we need to correctly infer the `key_type` based on the type of the key provided. In the cases provided by the failing test, the keys are strings, so the `key_type` should be inferred as a string.

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

    elif not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

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

By correcting the inference of `key_type`, the function should now correctly handle the indexing based on the type of key provided and pass the failing test cases.