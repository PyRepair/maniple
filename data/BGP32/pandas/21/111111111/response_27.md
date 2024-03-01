To fix the bug in the `_get_with` function, we need to ensure consistent behavior for all indexers (list, ndarrays, Index). Currently, the function is not handling list indexers correctly, which leads to a KeyError in certain cases.

Based on the failing test cases and the expected behavior:
- When accessing a Series with a key that is not present in the index, the function should raise a KeyError for all types of indexers (list, ndarray, Index) to maintain consistency.
- The function should handle list indexers in a way that aligns with the behavior of other indexers.

Here is the corrected version of the `_get_with` function:

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
        raise KeyError(f"None of {key} are in the index")

    if isinstance(key, (list, np.ndarray, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type != "integer":
        raise KeyError(f"None of {key} are in the index")

    if not self.index.isin(key).all():
        raise KeyError(f"None of {key} are in the index")

    return self.reindex(key)
```

In this corrected version, we explicitly check if the key is not present in the index and raise a KeyError accordingly for list indexers. This change ensures consistent error handling across different types of indexers.

By implementing these improvements, the `_get_with` function should now pass the failing test cases and provide the expected behavior.