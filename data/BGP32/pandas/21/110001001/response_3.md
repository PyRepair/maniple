The issue in the `_get_with` function lies in the key_type being incorrectly inferred as "string" in all cases, resulting in the wrong behavior and potentially causing the function to return unexpected results.

To fix the bug, we need to properly infer the data type of the key being passed to the function. Since the key can be of various types like list, ndarray, Index, etc., we should ensure that the key_type is correctly determined based on the type of the key being processed.

Here is the corrected version of the `_get_with` function:

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

    if not is_list_like(key):
        return self.loc[key]

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

By incorporating the correct inference of data types for the key, we can ensure that the function behaves as expected and returns the correct results for different types of keys being passed to it.