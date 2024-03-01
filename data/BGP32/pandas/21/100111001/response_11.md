### Bug Explanation
The bug occurs because the `_get_with` function is not handling the case where the key is provided as a `list`, `np.ndarray`, `pd.Index`, or `pd.Series`. The function incorrectly infers the `key_type` as `'string'` and then attempts to index using `reindex` based on this incorrect type, leading to a `KeyError` in the failing test.

### Bug Fix Strategy
To fix the bug in the `_get_with` function, we need to correctly handle the case where the key is a `list`, `np.ndarray`, `pd.Index`, or `pd.Series`. We should identify the type of the key properly and choose the appropriate method for indexing based on this type.

### Corrected Version of the Function
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
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, pd.Index, pd.Series)):
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

By making these changes in the function, it should now correctly handle the case where the key is a `list`, `np.ndarray`, `pd.Index`, or `pd.Series` and successfully pass the failing tests.