### Bug Explanation
The bug occurs because the `key_type` is incorrectly inferred as `'string'` for all cases, which leads to incorrect branching in the function and the wrong behavior when indexing the Series.

### Bug Fix Strategy
The issue lies in how the `key_type` is being inferred. To fix the bug, we need to properly infer the `key_type` based on the type of `key` being passed to the `_get_with` function.

### The Corrected Function
Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if is_list_like(key) and not isinstance(key, (np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Series):
        key = key.array

    key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        #  (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected function will correctly infer the `key_type` based on the type of `key` passed to the function, allowing for proper indexing behavior.