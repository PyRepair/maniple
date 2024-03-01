The bug in the `_get_with` function arises from the way it handles different types of indexers, specifically when a list indexer is used. It fails to properly detect non-match situations leading to unexpected behavior.

The key issue is the conversion of the key to a list without handling the case where the key is not present in the index. This results in returning the whole Series instead of raising an error when the key is not matched.

To fix this issue, we need to properly handle the case where the key is not found in the index. We can achieve this by adding a check to verify if the key is present in the index before proceeding.

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

    if not is_list_like(key):
        return self.loc[key]

    if key not in self.index:
        raise KeyError(f"None of {key} are in the index")

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

By adding the check `if key not in self.index`, we ensure that if the key is not found in the index, a `KeyError` will be raised correctly.

This correction aligns with the expected behavior outlined in the failing test cases and addresses the issue described in the GitHub report related to inconsistencies in handling different types of indexers.