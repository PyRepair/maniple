### Bug Explanation
The bug occurs in the `_get_with` function when the input key is a list, np.ndarray, Index, Series, or ExtensionArray. The function attempts to infer the type of the key but incorrectly identifies it as "string" in all cases. This leads to incorrect handling of the key and results in a KeyError when attempting to index the Series.

### Bug Fix Strategy
To fix the bug, we need to correctly identify the type of the key provided to the function. This can be achieved by updating the logic that infers the dtype of the key based on its type. We should correctly handle the different types of keys (list, np.ndarray, Index, Series, and ExtensionArray) and ensure that the key type is accurately identified.

### Corrected Code
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

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]

        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

With this corrected version of the function, the bug should be fixed, and the function should now correctly handle the different types of keys provided.