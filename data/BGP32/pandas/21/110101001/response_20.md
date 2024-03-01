### Bug Explanation
The bug occurs in the `_get_with` function of the `Series` class. When a non-list-like key is passed to the function, the function tries to access the key directly using `self.loc[key]`. However, in cases where the key is of type `Index` or `np.ndarray`, it should either be treated as a positional indexer (`self.iloc[key]`) or converted to a list beforehand.

### Bug Fix Strategy
To fix the bug, we need to update the logic for handling non-list-like keys. We should check if the key is of type `Index` or `np.ndarray`, convert it to a list if needed, and then decide whether to use `self.loc` or `self.iloc` based on the index type.

### Corrected Version
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
        key = [key]

    if isinstance(key, Index):
        key = key.tolist()

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index.is_all_dates:
            if not self.index.is_object() and self.index.is_unique:
                return self._get_values_tuple(key)
            else:
                return self.iloc[key]
        else:
            if self.index.is_object() or self.index.is_empty:
                return self._get_values_tuple(key)
            else:
                return self.iloc[key]

    return self.loc[key]
```

This corrected version correctly handles the various types of keys and ensures that the key is treated appropriately based on its type and the index type. This version should pass the failing test cases provided.