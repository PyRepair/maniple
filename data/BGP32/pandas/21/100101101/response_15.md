### Bug Explanation
The bug occurs because the function `_get_with` incorrectly infers the `key_type` variable as `'string'` in all cases, which leads to incorrect handling of the input `key` in the subsequent logic. This incorrect inference prevents the function from correctly identifying the type of the `key` input, causing the function to return incorrect results or raise errors unexpectedly.

### Bug Fix Strategy
To fix the bug, we need to update the logic for inferring the `key_type` based on the actual type of the `key` input. This will ensure that the function handles the input `key` correctly based on its type, leading to the expected behavior.

### Corrected Version of the Function
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

    elif not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

With the corrected version of the function, the type inference for the `key_type` variable will be based on the actual type of the `key` input, ensuring that the function processes the input correctly and returns the expected results for the failing tests.