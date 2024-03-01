### Analysis:
1. The `_get_with` function in the `Series` class is designed to handle different types of keys for indexing a series.
2. The bug seems to arise from the handling of non-list-like keys correctly.
3. The key_type is incorrectly determined as 'integer' for string keys, leading to incorrect behavior.
4. The GitHub issue highlights the inconsistency in behavior when indexing with a list that contains no matches.
5. The function needs to correctly identify the key type and handle non-list-like keys appropriately.

### Bug Fix Strategy:
1. Update the logic to correctly infer the key type for different types of keys.
2. Handle non-list-like keys in a consistent manner to avoid errors when indexing without matches.

### Corrected Version of the Function:
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

    if not is_list_like(key):
        return self.reindex(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list) and not isinstance(key, Index):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version should address the bug by correctly handling different types of keys for indexing a series, ensuring consistent behavior and avoiding errors when indexing without matches.