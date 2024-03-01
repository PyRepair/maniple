The bug in the `_get_with` function is caused by incorrect handling of the key type when `key` is not a list-like object. The function wrongly assumes that all non-list-like keys can be used directly with `self.loc[key]`, which results in a KeyError when accessing the Series.

To fix the bug, we need to properly handle non-list-like keys that are not recognized as scalars. We should first check if the key is a scalar using `is_scalar` and then proceed accordingly.

Here is the corrected version of the `_get_with` function:

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

    if is_scalar(key):
        return self.loc[key]

    if not is_list_like(key):
        key = [key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

This correction ensures that non-list-like keys are correctly handled based on whether they are scalars or not. It incorporates the `is_scalar` check before attempting to use `self.loc[key]`, preventing the KeyError from occurring in the failing test cases.

After applying this fix, the `_get_with` function should correctly handle the different types of keys as expected in the failing test cases.