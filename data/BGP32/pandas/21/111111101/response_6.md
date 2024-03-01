### Bug Explanation:
The bug occurs in the `_get_with` function when the type of the `key` parameter is not correctly handled. The function contains a conditional check for different types of `key` values, but it does not handle the case where the `key` is a list or ndarray properly. As a result, the function incorrectly infers the `key_type` as "string" instead of handling list-like input correctly.

### Bug Fix Strategy:
To fix this bug, we need to ensure that when `key` is list-like (list, ndarray, Index, Series), it is processed correctly. We should update the conditional check to handle list-like input appropriately, possibly by converting it to a list if needed and then proceeding with the logic based on the key type.

### Corrected Function:
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

By updating the function to correctly handle list-like input, it should now pass the failing test cases provided.