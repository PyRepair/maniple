### Analysis
The `key_type` variable is being incorrectly inferred as `'string'` in all test cases, but it should be inferred as `'object'` since the key values are strings. This incorrect inference leads to the wrong path being taken in the subsequent conditional statements in the `_get_with` function, causing the KeyError to not be raised as expected in the tests. The issue seems to be with the inference of the key type.

### Bug Explanation
The bug occurs due to the incorrect inference of the key type as 'string' instead of 'object'. This causes the function to take the wrong path in the `if key_type == "integer"` conditional block, leading to the incorrect return value instead of raising the KeyError as expected in the failing tests.

### Bug Fix
To fix the bug, we need to ensure that the key type is correctly inferred as 'object' when dealing with strings. We can modify the inference code to correctly determine the key type. 

### Corrected Version of the Function
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

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "string":
        key_type = "object"

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By correcting the inference of the key type in the function, the bug should be fixed, and the function should now correctly handle the keys and raise the expected KeyError in the failing tests.