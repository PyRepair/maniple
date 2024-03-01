### Bug Explanation
The bug occurs because the function `_get_with` does not handle the case where the key type is a string correctly. The function incorrectly assumes that the key type is "integer" when it should be inferred as a string. This leads to the function attempting to index the Series using an invalid index, resulting in a KeyError.

### Bug Fix Strategy
To fix the bug, the function should correctly infer the key type as a string when the key is not a list-like object. This will ensure that the function handles string keys correctly and prevents the KeyError from occurring.

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
        return self.loc[key] if key in self.index else self.reindex(key)

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

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

By checking if the key is in the index before trying to access it using `self.loc[key]`, we ensure that the correct behavior is maintained when dealing with string keys. This fix should address the KeyError issues in the failing test cases.