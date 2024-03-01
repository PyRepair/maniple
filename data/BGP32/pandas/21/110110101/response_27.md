### Bug Explanation:
The bug lies in the comparison check for the key_type in the `_get_with` function. The bug causes the function to incorrectly handle different types of keys, leading to unexpected behavior for non-integer keys. Specifically, the bug incorrectly infers the key_type as "integer" even for keys that are not of type integer, causing the function to take the wrong path in its logic.

### Fix Strategy:
To fix the bug, we need to correctly determine the key_type based on the type of key being passed to the function. We can achieve this by updating the logic that determines the key_type for different key types. By properly identifying the key_type, we can ensure that the function correctly handles different key types and returns the expected results.

### Corrected Function:
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, (pd.DataFrame, pd.Series)):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    elif isinstance(key, (list, np.ndarray, ExtensionArray, Series)):
        key_type = lib.infer_dtype(key, skipna=False)
    else:
        key_type = 'string'  # Assume key is of type string
    
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By incorporating the correct logic for determining the key_type based on the type of key being passed, the updated `_get_with` function should now correctly handle different key types and pass the failing test cases.