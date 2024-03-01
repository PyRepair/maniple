### Bug Explanation
The bug in the `_get_with` function occurs because the condition to check if `key` is of type `Index` is incorrect. The current implementation checks if `key` is an instance of `Index`, and if not, infers the type using `lib.infer_dtype`. This leads to issues when `key` is a `slice`, a `tuple`, or another non-`list_like` object, resulting in an incorrect `key_type`. Additionally, the condition to handle the case where `key` is a single value is incorrect, leading to another potential bug.

### Bug Fix Strategy
1. Update the check for `Index` type to use `isinstance(key, Index) or issubclass(type(key), Index)` to correctly identify instances of `Index`.
2. Modify the condition to handle non-`List_like` objects to correctly handle cases like `slice`, `tuple`, and individual values.
3. Add a check to handle the case when `key` is a single value more appropriately.

### Corrected Version of the Function
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
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
        key = [key]

    if isinstance(key, (Index, np.ndarray)):
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

By making these adjustments, the function should correctly identify the type of `key` and handle different input scenarios appropriately.