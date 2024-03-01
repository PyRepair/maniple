## Bug Analysis
The bug in the `_get_with` function lies in the handling of different types of keys. In the provided function:
1. When the key is a list, it attempts to reindex based on the key, which might lead to an incorrect result.
2. The key_type is determined incorrectly for certain types of keys.
3. Handling of Index objects is not consistent with other types of keys.

## Bug Fix Strategy
To fix the bug:
1. Ensure proper differentiation between different key types and handle them accordingly.
2. Update the determination of key_type to reflect the correct type.
3. Make sure the function returns the correct values based on the key type.

## Bug Fix
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

    if is_scalar(key):
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

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

With the provided bug fix, the function should now correctly handle different types of keys and return the expected results for each case.