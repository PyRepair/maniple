The bug in the `_get_with` function seems to be related to the handling of certain types of input `key`. The function is not properly distinguishing between different types of keys, leading to incorrect type inference in some cases, resulting in a `KeyError`.

### Bug Cause:
1. The function incorrectly categorizes the `key` variable as a string when it should recognize it as a list or ndarray.
2. The condition for filtering out certain types of keys is not properly defined, leading to incorrect handling of keys.

### Fix Strategy:
1. Update the function to properly identify the type of input `key` and handle each type accordingly.
2. Ensure the inferred type of the `key` is correctly determined to avoid errors during key-based operations.
3. Implement conditional checks to handle different key types appropriately.

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

    if not is_list_like(key) or isinstance(key, np.ndarray):
        key = list(key)

    if isinstance(key, (pd.Index, extension.Array)):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type in ("floating", "integer"):
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By updating the logic in the `_get_with` function as shown above, the function should now correctly handle different types of `key` inputs and avoid the `KeyError` that was occurring previously.