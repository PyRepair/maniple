## Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the `key` parameter when it is not a list-like object. Specifically, when `key` is not list-like, the function attempts to access the `key` index of the `self.loc` attribute, assuming `key` is a valid index. This will lead to an error if `key` is not a recognized index type.

## Bug Fix Strategy
To fix the bug, we need to properly handle cases where `key` is not list-like and ensure that the function returns the correct output based on the type of `key`.

## Corrected Function

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
    
    # Check if key is hashable
    if not is_list_like(key) and not is_scalar(key) and not isinstance(key, (Index, np.ndarray, ExtensionArray, Series)):
        return self.loc[key]

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

The corrected function now properly handles the case where `key` is not list-like and ensures that the appropriate action is taken based on the type of `key`.