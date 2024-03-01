### Bug Explanation
The bug occurs due to an incorrect evaluation of the `key_type` variable inside the `_get_with` function. The variable `key_type` is being inferred using the `lib.infer_dtype()` function based on the `key` input. In the failing cases, the `key` input is a string or a Series which results in the `key_type` being inferred as `'string'`. However, the subsequent logic in the function assumes that `key_type` should be `'integer'` for positional indexing. This leads to the incorrect execution path in the function causing the KeyError.

### Fix Strategy
To fix the bug, we need to ensure that the `key_type` is correctly inferred for the different types of `key` inputs. Specifically, for string inputs or Series inputs representing labels, the `key_type` should not be `'integer'`. We need to adjust the condition that determines the indexing behavior based on the `key_type`.

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

    if not is_list_like(key):
        # e.g. scalars that aren't recognized by lib.is_scalar, GH#32684
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type in ["string", "mixed-integer-float"]:
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

This corrected version of the function correctly infers the `key_type` and adjusts the indexing behavior based on the type of keys provided. It should now handle the different types of keys appropriately and pass the failing tests.