The bug in the `_get_with` function arises from the incorrect handling of the key type determination. The function incorrectly infers the key type using `lib.infer_dtype(key, skipna=False)` which leads to the key type being wrongly determined as "integer" even when it is a string or other types. This causes the function to use the wrong indexing method (`loc` or `iloc`), leading to unexpected results.

To fix this bug, we should determine the key type based on the actual type of the `key` parameter. We can achieve this by checking the type of the `key` parameter directly and then deciding on the appropriate indexing method (`loc` or `iloc`) based on the key type.

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

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = ensure_index(key)

    if key.inferred_type == "string":
        return self.loc[key]
    else:
        return self.iloc[key]
```

This corrected version directly checks if the key is a scalar using the `is_scalar` function and then proceeds accordingly. It also correctly handles the type of the `key` parameter and chooses the appropriate indexing method based on the key type. This approach ensures that the function behaves as expected for different types of keys.