The bug in the `_get_with` function lies in the incorrect handling of the key type. The function mistakenly identifies the key type as `'string'` instead of `'object'` when the key is an array-like object. This leads to incorrect behavior when trying to access the key from the Series.

To fix this bug, we need to ensure that the key type is correctly inferred when the key is an array-like object. We can do this by updating the `key_type` assignment to use the correct method for inferring the key type.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
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

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(np.asarray(key), skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By making this change, the function should now correctly infer the key type, allowing the tests to pass without raising a `KeyError`.