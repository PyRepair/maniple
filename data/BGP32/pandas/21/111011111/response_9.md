The issue in the `_get_with` function arises from how different types of indexers are treated inconsistently, leading to incorrect results and errors for certain cases. To address this, we need to adjust the logic in the function to handle all types of indexers consistently.

### Bug Explanation:
1. The `_get_with` function erroneously treats list-like indexers differently from other types like arrays or Index objects.
2. When providing a list indexer, the function does not handle it correctly, leading to KeyError exceptions.

### Fix Strategy:
1. Modify the logic to treat all indexers uniformly, regardless of their type, to ensure consistent behavior.
2. Address the KeyError issue caused by the current implementation.

### Corrected Version:
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

    key_arr = np.asarray(key)
    try:
        return self.loc[key_arr]
    except KeyError:
        return self.reindex(key_arr)
```

### Explanation of the Correction:
1. After detecting the type of the key, we convert it into a NumPy array (`key_arr`) to ensure uniform handling.
2. We then attempt to access the values using `self.loc` with the array.
3. If a KeyError occurs, we recover from the error by invoking `self.reindex` with the array key.

By employing this corrected version, the `_get_with` function should now properly manage all types of indexers consistently, resolving the KeyError issues and aligning with the expected behavior for different indexer types as outlined in the GitHub issue.