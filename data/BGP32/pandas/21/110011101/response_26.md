### Explanation:
The bug in the `_get_with` function arises from the incorrect handling of the key type when it is a list or ndarray. In the buggy code, when the key is a list or ndarray, it tries to perform operations based on the key's inferred type, which may not align with the actual type of the key.

Based on the failing tests and the provided runtime and expected values, the `key_type` is inferred as `'string'` in all cases, but the function logic does not take this into account properly.

### Bug Fix Strategy:
To fix the bug, we need to modify the logic related to determining the key type for lists and ndarrays. Since the key type is already inferred correctly as `'string'`, we can directly fall back to using `.loc` for indexing in these cases.

### Updated and Corrected Function:
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        #  or label-based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        return self.loc[key]

    return self.reindex(key)
```

By directly using `.loc` for indexing when the key is a list, ndarray, or Index, we ensure that the correct type inference is considered, and the function behaves as expected based on the provided use cases.