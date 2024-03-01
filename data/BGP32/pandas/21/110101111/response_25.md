The issue in the `_get_with` function arises from the handling of different types of indexers. Specifically, the function does not properly handle list indexers, leading to a KeyError when attempting to access values that are not present in the index.

To fix this bug, we need to ensure consistent behavior for all types of indexers and handle list indexers in a way that aligns with the other types (e.g., ndarray, Index). We can achieve this by updating the logic in the `_get_with` function to properly handle list indexers.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (np.ndarray, Index)):
        return self.loc[key]

    if isinstance(key, list):
        key = [x for x in key if x in self.index]
        if len(key) == 0:
            raise KeyError(f"None of {key} are in the index")
        return self.loc[key]

    return self.reindex(key)
```

This corrected version of the function ensures that list indexers are properly handled by checking if the elements are present in the index before attempting to access them. If none of the elements are found in the index, a KeyError is raised to maintain consistency with other types of indexers.

By implementing this fix, the `_get_with` function should now pass the failing test and align with the expected input/output values, resolving the issue reported on GitHub.