The bug in the `_get_with` function is due to incorrect handling of the input `key` when it is a scalar value. The function incorrectly assumes that the key type is `'integer'` when it is actually a string.

### Bug Explanation:
- The function `_get_with` checks the type of the input `key` and determines its type using `lib.infer_dtype`.
- When `key` is a scalar value (e.g., a single string), it is incorrectly identified as an integer type by `lib.infer_dtype` since it's not recognized as a scalar.
- This incorrect inference leads to the function assuming the key type is `'integer'`, causing the function to attempt to access the key as an integer index rather than a label-based index, resulting in a KeyError.

### Fix Strategy:
To fix the bug, we need to handle the case where the key is a scalar value, typically a string label. We can modify the function to specifically check for scalar values and handle them accordingly.

### Corrected Version of the `_get_with` function:
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
    elif is_scalar(key):
        # Handling scalar values (e.g., single string label)
        return self.loc[key]
    
    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By adding a specific check for scalar values using `is_scalar(key)` and handling them by using `self.loc[key]`, we can correctly handle cases where the key is a scalar value, such as a string label. This fix should address the KeyError issues encountered in the failing tests.