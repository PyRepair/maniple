### Analysis:
1. The buggy function `_get_with` in the `Series` class is designed to handle different types of input for indexing a `Series`.
2. The failing tests are related to using different types of indexers (`list`, `ndarray`, `Index`, `Series`) with no matches in the `Series` for retrieval.
3. The bug is likely caused by the inconsistent behavior of how list indexers are handled compared to other array-like indexers in the `_get_with` function.
4. The expected key_type inferred in the function before returning is `'string'`, but the bug causes a `KeyError` when handling certain index types with no matches.
5. To fix the bug, we need to ensure consistent behavior across different index types and handle cases where none of the keys matches the index appropriately.

### Bug Fix Strategy:
1. Modify the conditions in the `_get_with` function to ensure consistent behavior for different index types.
2. Handle the case where the key does not match any index values without causing a `KeyError`.
3. Update the logic to properly distinguish between list-like, array-like, and other index types for indexing the `Series`.

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
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if len(key) == 0:  # Handle case when key has no matches
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

    # handle the dup indexing case GH#4246
    return self.loc[key]
```

By incorporating the modifications as outlined above, the corrected version of the `_get_with` function should handle different index types consistently and appropriately manage cases where there are no matches, thus passing the failing tests.