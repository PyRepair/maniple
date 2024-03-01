### Bug Explanation
The bug in the `_get_with` function occurs when the `key_type` is incorrectly inferred as `'string'` for all input types, which leads to an incorrect path being taken in the function logic. The key_type should be inferred based on the type of the input `key`.

- For Case 1 and Case 2, the input `key` is a list or ndarray containing a string element, but the inferred type is `'string'` instead of `'object'`.
- For Case 3, the input `key` is an `Index` object, and the type is correctly inferred as `'object'`, yet the bug occurs further in the logic path.
- For Case 4, the input `key` is a Series object, but it is treated as a string during type inference.

### Bug Fix Strategy
To fix the bug, the type inference logic for `key` should be corrected to correctly identify the type of the input. Then, based on the type, the appropriate path should be taken in the function logic.

### Corrected Code
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind='getitem')
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if not is_list_like(key):
        return self.loc[key]

    # Correct type inference for key
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == 'boolean':
        if not com.is_bool_indexer(key):
            raise ValueError("Cannot index with non-boolean array containing NA / NaN values")
    
    if key_type == 'integer':
        if not self.index.is_fallback_available():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

With this correction, the `_get_with` function should now correctly handle the type inference for the input `key` and take the appropriate action based on the type of the input. This should resolve the bug and make the function behave as expected in the failing test cases.