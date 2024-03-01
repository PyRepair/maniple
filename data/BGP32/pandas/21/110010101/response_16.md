### Analysis:
1. The buggy function `_get_with` is used within the `Series` class to handle different types of key inputs for indexing a series.
2. The function checks the type of the input key and performs different operations accordingly.
3. The bug is likely in the checking and handling of different key types, leading to incorrect indexing behavior.
4. The bug causes a KeyError to be raised when indexing with a key that doesn't match any values in the series.
5. The function should correctly identify the key type and handle each type appropriately to prevent errors.

### Bug Cause:
The bug is likely caused by improper handling of the key type when processing the input for indexing. The function is not correctly identifying the key type, leading to a KeyError being raised when trying to index the series.

### Fix Strategy:
1. Correctly identify the key type by checking its class.
2. Handle different key types (list, ndarray, Index, Series) appropriately for indexing.
3. Make sure the function returns the expected value based on the key type.

### Corrected Function:
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
        key = [key]

    if isinstance(key, (Index, np.ndarray, ExtensionArray)):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if self.index._should_fallback_to_positional():
            return self.iloc[key]
        else:
            return self.loc[key]

    if not self.index.is_unique:
        return self.loc[key]

    return self.reindex(key)
```

This corrected function should properly handle indexing with different key types, ensuring that the KeyError issue is resolved.