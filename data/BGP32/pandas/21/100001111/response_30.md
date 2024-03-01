### Bug Explanation
The bug occurs in the `_get_with` function when handling various types of key inputs. The issue arises due to inconsistent handling between list and other types of key inputs. The function correctly handles list-like key inputs, but when dealing with other types such as an Index or ndarray, it results in unexpected behavior. This inconsistency violates the expected behavior outlined in the GitHub issue, leading to the bug.

### Bug Fix Strategy
To fix the bug, we need to ensure consistent handling of all types of key inputs within the `_get_with` function. The correction should align with the expected behavior described in the GitHub issue to resolve the inconsistency.

### Corrected Version
```python
# Corrected _get_with function
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, (ABCDataFrame, ABCSeries, Index, np.ndarray, ExtensionArray)):
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

    if key_type == "boolean":
        return self.loc[key]

    return self.reindex(key)
```

By modifying the function to handle all non-list key inputs consistently and aligning the behavior with the expected outcome, we have effectively fixed the bug. The correction should now fulfill the expected input/output values and resolve the inconsistency reported in the GitHub issue.