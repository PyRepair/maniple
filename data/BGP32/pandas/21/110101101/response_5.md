### Bug Explanation
The bug in the `_get_with` function occurs because the code incorrectly identifies the type of the key. In the provided cases, the key is a string, but the code identifies it as an integer. This results in the key being treated incorrectly, leading to a KeyError. The issue lies in the inference of the key type using `lib.infer_dtype(key, skipna=False)`.

### Bug Fix Strategy
To fix the bug, we need to ensure that the key type is correctly identified. We can achieve this by checking the type of the key directly before trying to infer the type. If the key is a string, we should handle it appropriately based on that type.

### Corrected Version
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

    if isinstance(key, str):
        return self.loc[key]

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = "other"  # Setting a default type for non-index keys

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version of the `_get_with` function will correctly handle string keys and avoid the KeyError issue encountered in the failing test cases.