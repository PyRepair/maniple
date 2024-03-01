### Explanation:
The bug in the `_get_with` function arises from the inconsistent handling of different types of indexers, specifically when they do not have matches in the index of the Series. When using a list as an indexer, the error message is not raised correctly due to the logic flow in the function.

In the failing test cases provided:
1. When a list `['C']` is used as an indexer, the error message raised should state that none of the items in the indexer are present in the Series index, but this is not happening.
2. The same issue occurs when an `ndarray` or `Index` are used as indexers.

The issue on GitHub highlights the inconsistency in behavior for different types of indexers and the need for a uniform approach.

### Fix Strategy:
To fix the bug, we need to modify the code flow when a list, ndarray, or Index indexer is used. Instead of raising an error incorrectly, we should ensure that the correct error message is raised when none of the indexer values are present in the Series index.

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

    elif not is_list_like(key):
        return self.loc[key]

    key = ensure_index(key)

    if not any(self.index.isin(key)):
        raise KeyError(f"None of {key} are in the index")

    # handle the dup indexing case GH#4246
    return self.loc[key]
```

In the corrected version, we convert the `key` to ensure it's an `Index` type, then we check if any of the values in the `key` are present in the Series index using `self.index.isin(key)`. If none of the values are present, we raise a `KeyError` with the appropriate error message. Otherwise, we return the located values as before.