### Bug Explanation
The bug in the `_get_with` function arises from incorrectly handling the key when it is passed as a list-like object (list, np.array, pd.Index, pd.Series). While trying to access the key in the Series object, it raises a KeyError instead of reindexing or properly handling the key.

The bug can be identified by analyzing the behavior when the key is given as a list-like object and comparing it with the expected behavior. The key should be reindexed, but instead, the buggy function raises a KeyError.

### Bug Fix Strategy
To fix this bug, we need to modify the part of the function that handles list-like keys. Specifically, we should update the code to reindex the Series with the key when it is a list, np.array, pd.Index, or pd.Series. This will ensure that the key is properly handled and no KeyError is raised.

### Corrected Function
```python
def _get_with(self, key):
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        # or label based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif not is_list_like(key):
        # Reindex the Series with the key if it is list-like
        return self.reindex(key)

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

By making this correction to the `_get_with` function, it should now properly handle list-like keys and reindex the Series correctly. This will ensure that the failing test cases pass without raising a KeyError.