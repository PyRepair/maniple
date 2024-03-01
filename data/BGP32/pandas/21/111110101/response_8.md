The bug in the `_get_with` function is due to the incorrect handling of the `key` parameter when it is not a list-like object. The function assumes that if `key` is not list-like, then it should be treated as a scalar index value and passed to `self.loc[key]`. However, this assumption is incorrect when dealing with non-list-like objects like arrays or Index objects.

To fix the bug, we need to update the handling of non-list-like `key` values to correctly identify and handle them according to their specific type. We should avoid treating them as scalar index values when they are not.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, (slice, ABCDataFrame)):
        raise TypeError("Indexing with slice or DataFrame is not supported.")
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    # Handle non-list-like objects
    if not is_list_like(key):
        if isinstance(key, (np.ndarray, ExtensionArray, Index)):
            return self.reindex(key)
        else:
            raise ValueError("Unsupported key type.")

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    return self.reindex(key)
```

This corrected version includes explicit handling for non-list-like objects such as arrays, Index objects, and other cases not covered by the original implementation. This should resolve the issue and pass the failing test cases.