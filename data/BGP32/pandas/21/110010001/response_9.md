### Analysis:
- The provided function `_get_with` is intended to handle different types of input keys, such as slices, DataFrames, tuples, scalars, lists, numpy arrays, etc., and return the corresponding values from the Series.
- The error messages indicate that the function is failing when trying to access values using certain types of keys like lists, arrays, and Series.
- The function needs to correctly handle the cases where the input key is a list, numpy array, Index, or another Series.

### Bug Cause:
- The bug occurs in the following lines of code:
    ```python
    elif not is_list_like(key):
        return self.loc[key]
    ```
- The `is_list_like` function is evaluating to `True` for Index objects, which leads to selecting values using `self.loc[key]`, causing a KeyError.

### Fix Strategy:
- Update the condition to handle Index, numpy arrays, and Series separately from regular list-like objects.
- Use `isinstance` checks to make sure the correct behavior is applied based on the type of the key.
- Directly return values based on the keys if they are Index, numpy arrays, or Series.
- Use `self.iloc` or `self.loc` for the appropriate types of keys.

### Corrected Function:
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

    # Handle key when it's an Index, numpy array, or Series
    if isinstance(key, (Index, np.ndarray, Series)):
        return self[key]

    if not is_list_like(key):
        # Handle non-list-like scalars (e.g., Index objects)
        return self.loc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By updating the function as per the suggested strategy, the corrected version should now handle the different types of keys appropriately, resolving the KeyError issues encountered in the failing tests.