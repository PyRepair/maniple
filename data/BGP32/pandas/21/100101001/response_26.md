### Bug Explanation
The bug in the `_get_with` function is caused by the incorrect handling of the `key_type` variable. In all test cases provided, the `key_type` is incorrectly inferred as `'string'` instead of the correct type. This incorrect type inference leads to the function attempting to handle the key as a string, resulting in the KeyError being raised because the key is not found in the index.

### Bug Fix Strategy
To fix the bug, we need to ensure that the `key_type` variable is correctly inferred based on the input key type. We can modify the logic to properly determine the type of the key and handle it accordingly to prevent the KeyError from being raised.

### Corrected Version of the Function

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

    elif not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer" or key_type == "string":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

With the updated code above, we have modified the key_type check to also consider the type 'string' when deciding how to handle the key. This should prevent the KeyError from being raised due to incorrect type inference.