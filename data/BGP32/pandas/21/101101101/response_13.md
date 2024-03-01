### Bug Explanation
The bug occurs in the `_get_with` function when handling the case where `key` is a list-like object but not recognized as a list, np.ndarray, ExtensionArray, Series, or Index. In this case, the function tries to access `loc` on the `self` Series using the `key`. If the `key` is not present in the index of the Series, a KeyError is raised.

The bug arises from not correctly identifying certain non-list objects as keys to be used for indexing. This can lead to unexpected behavior, such as trying to access a non-existent key in the index and raising a KeyError.

### Bug Fix Strategy
To fix the bug, we need to ensure that all non-list objects that are used as keys for indexing purposes are correctly handled. Specifically, we should check if the key is present in the Index of the Series before trying to access it using `loc`.

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

    if not is_list_like(key):
        key = [key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key] if key in self.index else self.reindex(key)
        else:
            return self.iloc[key] if key in self.index else self.reindex(key)

    if isinstance(key, list):
        return self.loc[key] if all(elem in self.index for elem in key) else self.reindex(key)
    
    return self.reindex(key)
```

With this correction, we first ensure that `key` is converted to a list if it is not already. Then, before trying to use `loc` or `iloc`, we check if all elements of the key are present in the index of the Series. If not, we fallback to using `reindex` to handle missing keys. This correction ensures that the function behaves as expected and does not raise unnecessary KeyErrors.