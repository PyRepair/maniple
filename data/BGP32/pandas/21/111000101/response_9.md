## Bug Analysis
The bug in the `_get_with` function occurs when the input `key` is a non-list-like scalar value. The function is intended to return the corresponding value from the Series using `self.loc[key]`. However, due to the bug, the function does not correctly handle non-list-like scalar values.

## Bug Explanation
When the input `key` is not list-like, the function attempts to access the value using `self.loc[key]`. However, this results in an error because the `key` is not an index. This causes the function to fail and output the incorrect result.

## Fix Strategy
To fix the bug, we need to modify the code to correctly handle non-list-like scalar values as input. We can check if the `key` is not list-like and then directly return the corresponding value from the Series using `self.loc[key]`.

## Corrected Code
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

    return self.reindex(key)
```

The corrected code checks if the input `key` is not list-like, and if so, directly returns the value from the Series using `self.loc[key]`. This modification ensures that the function handles non-list-like scalar values correctly without causing an error.