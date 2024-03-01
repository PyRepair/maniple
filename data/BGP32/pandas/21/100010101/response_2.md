### Bug Explanation
The bug in the `_get_with` function is caused by the incorrect handling of key types. The function is designed to handle different types of keys (such as slices, DataFrames, tuples, lists, etc.) while indexing a Series. However, the logic for identifying the type of key is flawed, leading to errors when trying to index the Series.

In the failing test cases provided:
1. The key is a list, but the function incorrectly identifies the type as a non-list-like scalar, leading to the error.
2. The key is an ndarray, but the function also incorrectly handles it, resulting in the error.
3. The key is an Index object, but the function does not correctly infer the type of the key, leading to the error.
4. The key is a Series, but the function misidentifies it as a list, which causes the error.

### Bug Fix Strategy
To fix this bug, we need to ensure that the function correctly identifies the type of key being passed and handles it appropriately. We should update the logic to handle different types of keys based on their actual type, rather than making incorrect assumptions.

### Corrected Function
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

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = [key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list) and all(isinstance(k, str) for k in key):
        return self.loc[key]
    
    return self.reindex(key)
```

With these updates, the function should now correctly handle different types of keys and resolve the issues identified in the failing test cases.