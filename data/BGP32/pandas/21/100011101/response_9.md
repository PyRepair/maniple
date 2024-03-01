### Bug Explanation
The bug in the `_get_with` function occurs due to an incorrect check for the type of `key` provided as input. The function incorrectly infers the type of `key`, leading to incorrect handling and hence causing the failing tests.

1. In the given failing tests, different types of `key` inputs are provided - a list, an array, an Index, and a Series.
2. The function wrongly infer the type of the `key` variable as `'string'` in all the cases. This leads to incorrect branching and causes the error.
3. Since the function incorrectly identifies the type of `key` as `'string'`, the subsequent logic in the function is applied incorrectly based on this wrong assumption. This leads to a KeyError as the function fails to correctly index the Series with the provided `key`.

### Bug Fix Strategy
To fix the bug in the function, we need to ensure that the type of `key` is correctly identified and that the appropriate logic is applied based on this correct type inference.

### Corrected Function
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determin if this slice is positional
        #  or label based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if is_list_like(key) and not isinstance(key, (Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        #  (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
``` 

By making the modifications above, we now correctly handle the type inference of `key` and apply the appropriate logic based on the type. This corrected function should now pass the failing tests and correctly index the Series without raising a KeyError.