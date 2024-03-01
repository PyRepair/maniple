## Bug Explanation
The bug in the `_get_with` function arises because the key type is incorrectly inferred as `'string'` in all test cases. This happens because the function does not handle the case where `key` is an ndarray or Index type correctly. Instead of correctly inferring the key type from the input, it assumes the key type is `'string'` by default, leading to incorrect behavior and the failing tests.

## Bug Fix Strategy
To fix the bug, we need to update the logic for inferring the key type from the `key` input. We should consider the key type based on the actual input type (ndarray, Index) rather than assuming it to be `'string'`. By correctly identifying the key type, we can then proceed with the appropriate indexing method.

## The Corrected Version of the `_get_with` Function
Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)

    elif isinstance(key, ABCDataFrame):
        raise TypeError("Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column")

    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif is_scalar(key):
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

        elif isinstance(key, list):
            return self.loc[key]

        return self.reindex(key)
```

By updating the logic to correctly infer the key type based on the input type, the corrected function should now handle the different types of `key` inputs properly and pass the failing tests.