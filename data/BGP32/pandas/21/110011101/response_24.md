### Bug Explanation:
The bug in the `_get_with` function lies in the logic of determining the `key_type`. The key_type is incorrectly inferred as `'string'` for all cases, regardless of the actual type of `key` provided.

### Bug Fix Strategy:
1. Update the logic for inferring the `key_type` based on the actual type of `key` provided.
2. Make sure to handle different types of `key` such as lists, numpy arrays, pandas Index, and pandas Series appropriately.
3. Ensure that the correct path is followed in the function based on the type of `key` to return the desired result.

### Corrected Version of the `_get_with` Function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if is_list_like(key) and not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

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

This corrected version of the function should correctly infer the type of `key` and handle different types of inputs appropriately, ensuring that the function returns the expected outputs for all cases mentioned.