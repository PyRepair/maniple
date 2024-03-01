## Bug Explanation
The bug in the `_get_with` function occurs when handling non-list-like keys, such as scalars like strings or integers. The function is incorrectly using `self.loc[key]` instead of `self.loc[key]` since the key is not list-like. This leads to a KeyError being raised when trying to access an index that does not exist in the Series object.

## Bug Fix
To fix the bug, we need to adjust the code to handle non-list-like keys correctly. We will update the function to use `self.loc[key]` when dealing with non-list-like keys to ensure proper indexing.

## Corrected Function
```python
def _get_with(self, key):
    # ...
    if not is_list_like(key):
        return self.loc[key]
    
    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    # Note: The key_type == "boolean" case should be caught by the
    #  com.is_bool_indexer check in __getitem__
    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        #  (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

By making this adjustment, the corrected function should now properly handle non-list-like keys and pass the failing test cases.