### Bug Explanation
The bug in the `_get_with` function arises from inconsistent handling of the `key` variable. The function incorrectly identifies the type of the `key` variable as `'string'` in all cases, irrespective of the actual type. This leads to incorrect logic execution within the function, especially when branching based on the type of `key`.

### Bug Fix Strategy
To fix the bug, we need to accurately identify the type of the `key` variable and ensure that the subsequent logic is consistent with the actual type. By resolving this type inconsistency, the function should be able to handle different types of `key` inputs correctly.

### Corrected Version of the Function
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

By accurately determining the type of the `key` variable and adjusting the subsequent logic based on the type, this corrected version of the function should handle different `key` inputs properly.