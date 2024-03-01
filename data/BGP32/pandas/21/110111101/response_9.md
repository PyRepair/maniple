The bug in the `_get_with` function arises from the incorrect type comparison when checking for key types. The function fails to handle certain key types properly, leading to the KeyError in the failing tests.

The issue arises when the key is an ndarray or an Index. The current implementation incorrectly handles these key types, leading to an incorrect key_type inference. To fix this bug:
1. Update the logic to properly handle ndarray and Index types.
2. Ensure that the key_type is correctly inferred for these key types.

Here is the corrected version of the `_get_with` function:

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

    if isinstance(key, (list, np.ndarray, pd.Index, Series)):
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

This corrected version addresses the issues with the key type inference and should now pass the failing test cases.