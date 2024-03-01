### Analysis
The `_get_with` function is designed to handle different types of keys for indexing a Series. However, there are some issues in the key handling logic within the function that are causing the failing tests.

### Bugs
1. The function is not correctly handling the case when the key is a list or an ndarray, resulting in the `KeyError` exceptions in the tests.

### Cause of the Bugs
1. When the key is a list or an ndarray, the function fails to correctly determine the key type and therefore does not handle the indexing appropriately.
2. The logic to infer the key type based on the key data is not working as expected.

### Fix Strategy
1. Fix the logic to correctly determine the key type for list and ndarray inputs.
2. Update the logic to handle list and ndarray keys appropriately based on their types.

### Solution
Here is the corrected version of the `_get_with` function:

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

    key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type in ['integer', 'boolean']:
        # Decide whether to use positional or label-based indexing
        if not self.index.is_all_dates:
            indexer = self.index.get_indexer(key)
            if np.all(indexer == -1):
                raise KeyError(f"None of {key} are in the index")
        return self.iloc[key]
    elif key_type == 'string':
        # strings are treated as labels, use loc
        indexer = self.index.get_indexer(key)
        if np.all(indexer == -1):
            raise KeyError(f"None of {key} are in the index")
        return self.loc[key]
    else:
        # Reindex for other types
        return self.reindex(key)
```

This corrected version should now handle list, ndarray, and Index keys appropriately and pass the failing tests.