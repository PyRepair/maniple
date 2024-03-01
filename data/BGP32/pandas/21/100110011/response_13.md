### Issue Analysis:
- The buggy function `_get_with` incorrectly handles the case when a list is used as an indexer.
- The failing test `test_getitem_no_matches` is designed to test various types of objects as indexers (list, array, Index, Series).
- The error message indicates that the KeyError is not being raised as expected when using a list as an indexer.

### Error Location:
- The bug is likely in the following code block:
```python
if not is_list_like(key):
    return self.loc[key]
```
- The function incorrectly attempts to use `self.loc[key]` for non-list-like indexers.

### Bug Cause:
- The bug arises from the incorrect handling of list-like indexers in the `_get_with` function.
- When a list is used as an indexer, the function should raise a KeyError to match the behavior with other types of indexers.

### Fix Strategy:
- Update the condition that checks for list-like indexers to raise a KeyError for consistency.
- Modify the conditional block that handles non-list-like indexers appropriately.

### Corrected Version:
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
        if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
            key = list(key)
        else:
            raise KeyError(f"None of [{key}] are in the [index]")

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

### Conclusion:
- The corrected version of the `_get_with` function should now handle list-like indexers correctly and raise a KeyError when needed. This change aligns the behavior with other types of indexers and fixes the bug reported in the failing test.