### Bug Explanation
The bug occurs because the function `_get_with` incorrectly assumes the type of the `key` parameter based on its value's type. This leads to the `key_type` being incorrectly inferred as `'string'`. The key error here is in the handling of different key types.

### Bug Fix Strategy
We need to update the logic in the `_get_with` function to correctly handle different key types and infer the `key_type` based on the type of the key parameter, rather than its value's type. This can be achieved by checking the type of the `key` parameter directly.

### Corrected Version

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        # or label based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    # Handle different key types
    if is_list_like(key) and not isinstance(key, (np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)
    
    if isinstance(key, (list, Index)):
        key_type = key.inferred_type if isinstance(key, Index) else key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        # (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        # Handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

In the corrected version, we added additional checks to properly handle different key types and correctly infer the `key_type` based on the type of the `key` parameter. This should address the bug and ensure that the function behaves as expected in all cases.