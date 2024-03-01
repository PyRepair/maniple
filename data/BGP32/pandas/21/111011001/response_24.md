### Analysis
The `_get_with` function is supposed to handle different types of keys to extract values from the Series. However, the bug occurs when the key is a list or an ndarray, resulting in a KeyError not being raised as expected in the test cases.

Looking at the implementation, the bug arises when the `key_type` is determined to be `"string"` for list-like keys, leading to an incorrect branch of the conditional statements. This causes the function to not raise a KeyError when it should.

### Suggested Fix
To fix the bug, we need to correct the conditional check for list-like keys. The key should not be treated as a position indexer in this case, so we need to handle it differently.

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

    elif not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

In this corrected version, we removed the incorrect handling of list-like keys as positional indexers when `key_type` is determined to be `"string"`. Instead, we directly use `loc` to get the values for list-like keys.