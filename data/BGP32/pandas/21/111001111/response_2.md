The bug in the `_get_with` function lies in how different types of indexers are handled. In the provided cases, when a list-like key is passed, it is not properly handled, leading to incorrect behavior. The expected behavior should match that of array-like indexers rather than raising an error or returning incorrectly.

To fix the bug, we need to adjust the treatment of list-like indexers to align with array-like indexers for consistency. By properly handling list-like indexers, we can ensure that the function behaves as expected and avoids errors.

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

    elif is_list_like(key):
        return self.loc[key]

    return self.reindex(key)
```

By using `is_list_like(key)` instead of `not is_list_like(key)` and treating list-like key indexers in a similar way to other array-like indexers, we ensure proper handling and consistent behavior across different types of indexers. This correction addresses the issue reported on GitHub and aligns the function with expected input/output values for the provided test cases.