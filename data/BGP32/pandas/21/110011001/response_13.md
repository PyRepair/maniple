### Bug Explanation
The bug in the `_get_with` function arises from the conditional checks on the `key` parameter. When the `key` parameter is provided as a list, numpy array, or Series, the function fails to handle it correctly, resulting in a KeyError when trying to access non-existent indices from the main Series.

### Bug Fix Strategy
To fix the bug, we need to revise the conditional checks and handling of the `key` parameter. We should ensure that the correct type of the `key` is identified and processed accordingly to prevent KeyError exceptions.

### Corrected Version of the `_get_with` Function

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

    elif is_scalar(key):
        return self.loc[key]

    if is_list_like(key) or isinstance(key, (np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        if key_type in ["string", "integer"]:  # Update based on expected types
            use_loc = self.index.inferred_type != "integer"
            return self.loc[key] if use_loc else self.iloc[key]

    return self.reindex(key)
```

This corrected version of the `_get_with` function handles the different types of `key` parameters appropriately, ensuring that the correct indexing method (`loc` or `iloc`) is used based on the inferred type. This should prevent the KeyError exceptions seen in the failing tests.