### Bug Analysis:
The bug in the `_get_with` function arises from the incorrect handling of the `key` parameter when it is not a list-like object. The function incorrectly assumes that non-list-like keys are scalars that can be directly used for indexing through `self.loc[key]`, which leads to errors when the key is of type `string`.

### Bug Explanation:
- In Case 1 and Case 2, the `key` is being considered a list, but it is actually an ndarray and a string, causing the function to misinterpret the type.
- In Case 3, `key` is of type `Index`, and `key_type` is set incorrectly as `'string'`.
- In Case 4, `key` is a Series object, and once again, `key_type` is erroneously labeled as `'string'`.

### Bug Fix:
To fix the bug, we need to make sure that the key is correctly identified as a list-like or non-list-like object and handle each case appropriately.
Here is the corrected version of the `_get_with` function:
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
        # Handle non-list-like keys
        return self.loc[key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
            # Depending on the scenario, you may need to use iloc instead:
            # return self.iloc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By correctly distinguishing between list-like and non-list-like keys and handling each case appropriately, the bug in the `_get_with` function should be fixed.