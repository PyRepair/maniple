### Bug Explanation
The bug in the `_get_with` function lies in the `key_type` determination logic. Even though the input key is a list or array of strings, the function incorrectly infers the `key_type` as `'string'` instead of `'object'`. This incorrect inference leads to incorrect handling of the key, resulting in a `KeyError` during the test execution.

### Bug Fix Strategy
To fix this bug, we need to ensure that the `key_type` is correctly inferred based on the actual data type of the key. Specifically, if the key is a list, array, or Index of strings, the `key_type` should be inferred as `'object'`.

### Corrected Version of the Function
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

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == 'object':
        # handle the case where key is an array of strings
        return self.loc[key]

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version should properly handle the case where the key is a list, array, or Index of strings by inferring the `key_type` as `'object' and returning the corresponding values from the Series.