To fix the bug in the `_get_with` function, we need to handle the case where the `key` parameter is a list correctly to ensure consistency with the behavior of other indexers. Currently, when `key` is a list, the function is calling `self.reindex(key)` instead of `self.loc[key]`. This leads to inconsistent behavior compared to other indexers and might cause unexpected KeyError or NaN values.

Here is the corrected version of the `_get_with` function:

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

    elif is_list_like(key):
        return self.loc[key]

    return self.reindex(key)
```

In the corrected version:
- We added a check `is_list_like(key)` to correctly handle the case where `key` is a list.
- If `key` is list-like, we directly return `self.loc[key]` to maintain consistency with other indexers.
- For any other type of key, the function will fall back to `self.reindex(key)`.

This fix ensures that when `key` is a list, it will be processed correctly within the `_get_with` function. It aligns the behavior of list indexers with other types of indexers and resolves the inconsistent behavior reported in the GitHub issue.