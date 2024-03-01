The bug in the `_get_with` function arises from the inconsistent handling of different types of indexers, specifically in the case of a list indexer causing a `KeyError` when trying to access a non-existing index.

The bug is evident in the failing test `test_getitem_no_matches` where various types of indexers are tested, and the behavior for list indexers differs from other types like arrays, Index, and Series.

To fix the bug, we should treat list indexers consistently with other types of indexers. Instead of directly trying to reindex using a list indexer, we should handle it similarly to other types by converting it to an array-like structure.

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

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
        
    key_arr = np.array(key) if not isinstance(key, np.ndarray) else key

    return self.reindex(key_arr)
```

By converting the list indexer `key` into an array-like structure `key_arr`, we ensure consistency in handling all types of indexers, resolving the issue of causing `KeyError` for list indexers specifically in the failing test case.

This corrected version should now pass the failing test cases and align with the expected input/output values, as well as resolve the issue reported on GitHub regarding the inconsistency in handling different types of indexers.