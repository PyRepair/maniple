### Analysis
The `_get_with` function is designed to handle different types of key inputs and perform indexing operations accordingly. In the failing test cases, the function fails to raise a `KeyError` as expected when indexing with mismatched values.

The bug seems to be related to the logic for handling different types of key inputs and determining the appropriate type of indexing to perform.

### Bug Explanation
1. In the cases where the key parameter is a list of values or an ndarray, the function incorrectly infers the `key_type` as `'string'` due to the call to `lib.infer_dtype(key, skipna=False)`. This leads to incorrect indexing decisions and results in unexpected behavior.
2. The logic for handling key types like `list`, `np.ndarray`, `ExtensionArray`, `Series`, or `Index` is inconsistent and does not cover all possible scenarios, resulting in the function not behaving as expected.

### Bug Fix
To fix the bug, we need to:
1. Ensure that the `key_type` is correctly inferred for different key types by modifying the logic that determines the type.
2. Review and adjust the conditional statements to cover all possible key types and ensure that the correct indexing method is used depending on the key type.

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

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

With this corrected version, the function should correctly handle the different types of key inputs and perform the appropriate indexing operations, thereby passing the failing tests.