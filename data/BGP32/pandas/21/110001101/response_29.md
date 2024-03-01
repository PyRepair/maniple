### Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the `key_type` variable. In the cases provided, the `key_type` variable is wrongly assigned the value `'string'` instead of `'object'` when the `key` variable is a string or a list containing strings. This incorrect assignment leads to unexpected behavior in the subsequent conditional blocks, causing the function to return undesired results.

### Bug Fix Strategy
To fix the bug, the `key_type` variable assignment should be corrected to infer the actual type of the `key` input parameter. By ensuring that the correct type is assigned to `key_type`, the conditional blocks in the function can accurately determine how to handle the input, leading to the expected behavior.

### Corrected Function
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

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

By applying this correction, the `_get_with` function should handle the input key types correctly and return the expected results as described in the provided test cases.