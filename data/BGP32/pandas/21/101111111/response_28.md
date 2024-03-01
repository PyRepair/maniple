To fix the issue in the `_get_with` function, we need to handle the case when the key is a list or an ndarray correctly. Currently, the function mistakenly tries to treat all array-like indexers as Index objects, leading to the KeyError when using a list as the key.

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

    # Handling list or ndarray key correctly
    key = ensure_index(key)

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if key.inferred_type == "integer" and not self.index._should_fallback_to_positional():
        return self.loc[key]
    else:
        return self.iloc[key]
```

This corrected version ensures that the key is properly converted to an Index object, allowing the function to handle list and ndarray keys correctly without causing a KeyError.

By implementing this fix, the `_get_with` function should now behave consistently for list and ndarray indexers, resolving the issue reported on GitHub.