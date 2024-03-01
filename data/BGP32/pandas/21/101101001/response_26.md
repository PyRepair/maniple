## Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the `key_type`. The function incorrectly identifies the `key_type` as `'string'` even when the key is actually a list, ndarray, Index, Series, or an ExtensionArray. This leads to the function taking the wrong path when deciding whether to use `self.loc[key]` or `self.iloc[key]`, resulting in a KeyError.

## Fix Strategy
To fix the bug, we need to correctly identify the `key_type` based on the type of input `key`. Specifically, we need to check if the `key` is an instance of list, np.ndarray, Index, Series, or ExtensionArray and then determine the appropriate `key_type` based on that. With the correct `key_type`, the function should be able to handle the input key properly.

## Corrected Version of the `_get_with` Function
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

    elif is_scalar(key) or is_iterator(key):
        return self.loc[key]

    if is_list_like(key):
        key = list(key)

    if isinstance(key, (Index, np.ndarray, ExtensionArray, Series)):
        key_type = getattr(key, "inferred_type", lib.infer_dtype(key, skipna=False))
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

The corrected version of the `_get_with` function now properly identifies the `key_type` based on the type of input `key`. This should fix the bug and allow the function to handle different types of keys correctly.