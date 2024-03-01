### Bug Fix

The bug in the `_get_with` function is related to the way the key type is being inferred and handled. The key type is incorrectly inferred as "string" in all cases, leading to the `KeyError` when trying to access a key that is not present in the index.

To fix this bug, we need to properly infer the key type based on the input key. We can achieve this by modifying the code to check the type of the key and infer its type accordingly.

Here is the corrected version of the `_get_with` function:

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

    if is_scalar(key) and not is_string(key):
            return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
            key = list(key)

    if isinstance(key, (Index, Series)):
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

This fix corrects the key type inference to handle different types of keys properly, preventing the `KeyError` from being raised in the tests.