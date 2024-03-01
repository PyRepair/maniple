### Bug Explanation:
The bug in the `_get_with` function occurs when the `key` parameter is a single-element list or an ndarray of dtype object. In this case, the function incorrectly infers the `key_type` as `'integer'` even though it should be `'string'`. This leads to the function trying to index the Series using `self.iloc[key]` instead of `self.loc[key]`, resulting in a KeyError.

### Bug Fix Strategy:
To fix the bug, we need to correctly identify the `key_type` based on the data type of the elements in the `key` parameter. Since the elements in the `key` parameter are strings in the failing test cases, we should update the logic in the function to correctly infer the `key_type` as `'string'` in such cases.

### Corrected Function:
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

    elif not is_list_like(key):
        # e.g. scalars that aren't recognized by lib.is_scalar, GH#32684
        return self.loc[key]
    
    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "string":  # Update to correctly check for 'string' type
        return self.loc[key]
    
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

By updating the logic to correctly identify the `key_type` as `'string'` when the keys are strings, the corrected function should now return the expected output and pass the failing test cases.