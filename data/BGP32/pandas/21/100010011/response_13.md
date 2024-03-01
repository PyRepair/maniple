### Analysis:
The function `_get_with` is responsible for handling various types of indexers like a slice, DataFrame, tuple, scalar, list, etc. The bug is occurring when a `KeyError` is raised due to inconsistency in treating different types of indexers, specifically list indexers.

### Error Cause:
The bug is caused by inconsistency in handling different types of indexers within the `_get_with` function. When a list indexer is passed, the function is trying to reindex with that list causing a `KeyError` to be raised. This behavior is inconsistent with how other indexers are treated.

### Fix Strategy:
We need to ensure that list indexers are handled consistently with other types of indexers, especially when reindexing the Series.

### Corrected Code:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determin if this slice is positional
        #  or label based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif not is_list_like(key) or isinstance(key, (np.ndarray, Index)):
        if not is_list_like(key):
            key = np.array(key)
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        # Note: The key_type == "boolean" case should be caught by the
        #  com.is_bool_indexer check in __getitem__
        if key_type == "integer":
            # We need to decide whether to treat this as a positional indexer
            #  (i.e. self.iloc) or label-based (i.e. self.loc)
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]

        if key_type == "list":
            return self.loc[key]

    return self.reindex(key)
```

### Explanation:
- We added a condition to check if the key is a numpy array or an Index. If it is, we convert it to a numpy array, ensuring a consistent type for handling other than list-like indexers.
- Then, we check if the key type is "list" and use `self.loc` to handle the list indexer, ensuring consistent behavior with other types of indexers.
- These changes help in resolving the inconsistency in handling list indexers within the `_get_with` function.