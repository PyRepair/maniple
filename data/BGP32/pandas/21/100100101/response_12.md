### Analysis:
The bug in the `_get_with` function lies in the check for the `key_type == "integer"` condition. The function incorrectly assigns the key_type as `'string'` instead of `'object'` when dealing with keys of type `ndarray` or `Index` containing strings.

### Bug Explanation:
When providing a key as an `ndarray` or `Index` containing strings, the `_get_with` function incorrectly identifies the key_type as `'string'` instead of `'object'`. This leads the function to branch into the positional indexer path instead of the label-based indexer path, resulting in a misinterpretation of the key for indexing the Series.

### Bug Fix Strategy:
To fix the bug, we need to correctly infer the `key_type` based on the actual data type of the key provided, especially when the key is an `ndarray` or an `Index` containing strings.

### Corrected Version of the Function:
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

    elif not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer" or key_type == "string":  # Corrected condition here
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By updating the `key_type` condition to include `'string'` along with `'integer'`, we ensure that keys containing strings (`ndarray` or `Index`) are correctly handled as label-based indexing. This correction will enable the function to return the correct result for cases where the bug was previously causing issues.