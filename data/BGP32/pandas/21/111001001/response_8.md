The bug in the `_get_with` function lies in the logic for determining the `key_type`. The function incorrectly identifies the `key_type` as `'string'` in all cases, which leads to incorrect branching decisions later in the function.

### Bug Cause:
The bug arises due to the improper identification of the `key_type` based on the input `key`. The function mistakenly assigns a fixed value `'string'` to `key_type` regardless of the actual type of `key`, which causes the function to take unintended paths in the branching logic.

### Bug Fix Strategy:
To fix the bug, we need to correctly infer the `key_type` based on the type of `key`. We can utilize the information present in the function to determine the `key_type` accurately for different types of `key` inputs.

### Corrected Version of the `_get_with` function:

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

    elif is_scalar(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        if key_type in ['integer', 'mixed-integer']:
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]

        elif key_type == "boolean":
            return self.loc[key]

    return self.reindex(key)
```

By distinguishing the different types of `key` inputs and inferring the `key_type` appropriately, the corrected function will handle the indexing cases correctly based on the actual data types of the keys passed to it.