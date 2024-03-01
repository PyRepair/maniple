### Bug Analysis
The bug occurs because the function `_get_with` in the `Series` class is incorrectly handling the case of key as a list, array, Index, or Series. The function checks if the key is not list-like or an instance of specific types, and then tries to infer the key type based on the input key. However, in the cases provided:
1. The inferred key type is `'string'` which causes the function to fall into the last `else` block.
2. The correct key type should have been `'object'` for the input type.
3. Due to this incorrect inference, the function is not properly handling the key which leads to a `KeyError` when indexing the Series.

### Bug Fix Strategy
To fix the bug, we should ensure that the key type is inferred correctly based on the input key type. If the input key is a list, array, Index, or Series, the inferred type should be `'object'`, allowing the function to handle the key appropriately.

### Corrected Version
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

    key_type = lib.infer_dtype(key, skipna=False)  # Infer key type correctly

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):  # Check for list-like types
        if isinstance(key, Index):  # Corrected block for Index
            key_type = key.inferred_type
        else:
            key_type = "object"  # Assign correct type for list-like keys

    if key_type == "object":  # Check for the correct key type
        return self.reindex(key)

    raise TypeError("Unsupported key type: {}".format(key_type))  # Handle unsupported key types
```

By correcting the key type inference and branching based on the correct key type, the function should now handle list, array, Index, and Series keys correctly, resolving the `KeyError` issues in the failing tests.