The bug in the `_get_with` function stems from the misinterpretation of the key type, leading to incorrect handling of the key input. The function incorrectly assumes that the key type is always determined as an integer or list-like, leading to errors when the key is a string type.

To fix the bug:
- We need to ensure that the key type is correctly identified based on the input type.
- Modify the conditional statements to handle different key types appropriately.

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

    if is_scalar(key):
        return self.loc[key]

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

This corrected version includes proper handling of scalar keys by using the `is_scalar` function to detect scalar values. Additionally, the conditionals have been adjusted to correctly handle different key types, ensuring that the key is treated appropriately based on its type.