### Bug Explanation
The bug in the `_get_with` function arises from the incorrect comparison of the inferred type of the key with the string `"integer"` and the subsequent decision on whether to treat it as a positional indexer or label-based indexer. The bug is specifically due to the fact that the key type is being incorrectly inferred as `"string"` in all cases, leading to incorrect indexing.

### Bug Fix Strategy
To fix the bug, we need to ensure that the key type is correctly inferred and compared with `"integer"` to determine the indexing strategy. This can be achieved by appropriately handling the types of keys being passed to the function and ensuring that the key type is accurately identified.

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

By correcting the comparison based on the inferred `key_type` correctly, the function will now accurately determine how to handle different types of keys and perform the indexing operation as expected.