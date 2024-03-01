### Bug Analysis
The buggy function `_get_with` is intended to handle different types of keys for indexing a Series object. The bug appears to be related to how the function handles keys with no matches in the index. The key_type is incorrectly identified as 'string' in all cases where the input key does not match any index values.

### Bug Explanation
When the function encounters a key that has no matches in the index, it should raise a KeyError with a specific message indicating that none of the index values match the key. However, due to the mishandling of such cases, the key_type is incorrectly identified as 'string', leading to unexpected behavior and failing test cases.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly identifies the key type and raises a KeyError with the appropriate message when the key does not match any index values. We should update the logic to handle such cases appropriately and provide a more informative error message to signal the issue.

### Corrected Function
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

    if not is_list_like(key):
        raise KeyError(f"None of {key} are in the index")

    if not any(self.index.isin(key)):
        raise KeyError(f"None of {key} are in the index")

    if isinstance(key, (Index, list)):
        key_type = key.inferred_type if isinstance(key, Index) else lib.infer_dtype(key, skipna=False)

        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]

        if key_type == "boolean":
            raise KeyError("Boolean indexing not supported")
        
    return self.reindex(key)
```

By making these changes, the function should now correctly handle cases where the key does not match any index values and raise a KeyError with the appropriate message. This should resolve the bug and ensure that the failing test cases pass as expected.