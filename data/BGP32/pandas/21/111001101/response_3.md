### Bug Explanation
The bug in the `_get_with` function arises from incorrectly inferring the `key_type` variable. In the provided cases, the key_type is always assigned the value `'string'`, regardless of the actual type of the `key`. This inconsistency causes incorrect branching in the function and leads to unexpected behavior.

### Bug Fix Strategy
To fix the bug, we need to correctly infer the type of the `key` parameter and adjust the behavior accordingly. We should ensure that the `key_type` variable accurately reflects the type of the `key`.

### Corrected Version of the Function
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        #  or label-based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

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

In this corrected version, we calculate the `key_type` based on the inferred type of the `key` parameter using the `lib.infer_dtype` function. This ensures that the branching logic in the function aligns with the actual type of the `key` being passed.