### Bug Analysis
In the provided function `_get_with`, the bug is likely related to how it handles different types of keys, specifically when the key is a list, ndarray, Index, or Series. 

1. When the key type is a list or ndarray, the function incorrectly infers the key type as "string" due to improper handling of list-like objects.
2. The function doesn't handle the case properly when the key is an Index, resulting in a KeyError when trying to access an element in the Series.

### Bug Fix Strategy
1. Update the function to properly handle different types of keys. Specifically, ensure that the key type is correctly inferred for list-like objects.
2. Add a specific condition to handle cases where the key is an Index to prevent KeyError exceptions.

### Corrected Function
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

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = lib.infer_dtype(key, skipna=False)

        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]

        elif key_type == "string":
            return self.loc[key]

    return self.reindex(key)
```

By adding appropriate checks and handling of the different key types, especially for Index objects, the corrected function should no longer raise KeyError exceptions and pass the failing tests.