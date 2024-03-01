## Bug Explanation
The bug in the `_get_with` function arises from an incorrect check for whether the `key` input is a list-like object. The current implementation checks if `key` is not a list-like object by using `not is_list_like(key)`. However, this condition will incorrectly evaluate to `True` for list-like objects, leading to unexpected behavior in the function.

## Bug Fix Strategy
To fix the bug, the condition checking whether `key` is not a list-like object should be corrected to properly handle list-like objects. This can be achieved by using a condition that checks if `key` is a list-like object.

## Code Correction
```python
    def _get_with(self, key):
        # other: fancy integer or otherwise
        if isinstance(key, slice):
            # _convert_slice_indexer to determine if this slice is positional
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
        
        elif isinstance(key, (np.ndarray, ExtensionArray, Series, Index)):
            key_type = lib.infer_dtype(key, skipna=False)

            if key_type == "integer":
                # We need to decide whether to treat this as a positional indexer
                #  (i.e. self.iloc) or label-based (i.e. self.loc)
                if not self.index._should_fallback_to_positional():
                    return self.loc[key]
                else:
                    return self.iloc[key]

            # handle the dup indexing case GH#4246
            return self.loc[key]
    
        return self.reindex(key)
```

By making the above correction, the function will now correctly handle list-like objects for the `key` parameter and should behave as intended in all test cases provided.