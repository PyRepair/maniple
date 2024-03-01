### Analysis:
1. The buggy function `_get_with` is designed to handle different types of indexing, such as slice, DataFrame, tuple, list-like, and reindexing.
2. The failing test cases encounter issues when passing a list, ndarray, Index, or Series to the Series object for indexing, leading to a KeyError as none of the values in the passed index match the Series index.
3. The key_type is inferred as 'string' in all failing test cases, which is incorrect.
4. The failing tests aim to cover consistent behavior for list/ndarray/Index/Series indexing methods.

### Bug Cause:
The bug is likely due to incorrect key_type inference which results in treating the provided key differently than expected, leading to a KeyError when the key is used for indexing.

### Bug Fix Strategy:
Modify the key_type inference logic to correctly identify the type of key being passed for indexing. Ensure that the function behaves consistently for list, ndarray, Index, and Series indexers.

### The Corrected Version of the Function:
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

    # Correct key_type identification
    key_is_list_like = is_list_like(key)
    key_has_bool_indexer = is_bool(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_has_bool_indexer and not key_is_list_like:
        raise KeyError(f"None of {key} are in the index")

    if key_type in ["integer", "mixed-integer"]:
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if key_is_list_like and not key_has_bool_indexer:
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

By making the necessary corrections to the key_type identification and handling edge cases for list-like and bool indexers, the corrected function should work consistently for list, ndarray, Index, and Series indexers. This fix aligns with the expected behavior described in the failing tests and the GitHub issue.