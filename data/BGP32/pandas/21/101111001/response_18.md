### Bug Explanation
The bug occurs because the key_type is incorrectly inferred as `'string'` in all cases. This leads to the wrong execution path within the `_get_with` function. The code path that handles the case when key_type is "integer" is not being taken as expected.

### Bug Fix Strategy
To fix the bug, we need to ensure that the key_type is correctly inferred based on the type of key being passed to the `_get_with` function. This will enable the function to properly handle different types of keys, such as integers, lists, etc.

### Corrected Version of the Function

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

    elif not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

With this correction, the `_get_with` function should correctly handle different types of keys and infer the key_type accurately based on the input key.