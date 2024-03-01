### Bug Explanation
The bug occurs in the `_get_with` function when checking the type of the `key` parameter. The function incorrectly identifies the key type as a string (`key_type = 'string'`) for various types of keys that should be handled differently. This leads to incorrect indexing operations and results in a `KeyError` being raised.

### Bug Fix Strategy
To fix the bug, we need to correctly determine the type of the `key` parameter and handle different types appropriately. We should ensure that the key type is accurately identified to perform the corresponding indexing operation without raising errors.

### Corrected Function
Here is the corrected version of the `_get_with` function:

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

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

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

With this corrected version, the function should now correctly identify the type of the `key` parameter and handle different key types accordingly, avoiding the `KeyError` that was raised in the failing tests.