### Bug Analysis
The bug seems to be related to how the function handles the case when `key` is an ndarray, Index, or Series, resulting in a KeyError during indexing.

### Bug Explanation
1. In Case 1 and Case 2, the function determines the `key_type` as `'string'`, which is incorrect. This leads to the wrong path being taken in the subsequent logic.
2. When `key` is an Index, as seen in Case 3, the `key_type` is inferred correctly as `'string'`. However, the function still returns the wrong result, leading to a KeyError.
3. The function's logic to handle different types of `key`s leads to incorrect indexing or reindexing operations, resulting in KeyError.

### Bug Fix
To fix the bug, we need to ensure the correct handling of different data types in the `key`. We can simplify the logic by enabling appropriate indexing based on data type.

### Corrected Function
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    if isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )

    if isinstance(key, tuple):
        return self._get_values_tuple(key)

    if is_list_like(key):
        return self.loc[key]

    if is_int(key):
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected function should handle the different types of `key` appropriately and avoid the KeyError issue encountered in the failing tests.