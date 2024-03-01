### Bug Explanation:
The bug occurs in the `_get_with` function when dealing with different types of key inputs. The issue arises when a key of type `Index` is passed, leading to incorrect handling. The function wrongly determines the key type as `'string'`, which results in returning unexpected results or errors.

### Bug Fix Strategy:
To fix the bug, we need to ensure proper handling of keys of type `Index` and accurately determine the key type based on the provided key input.

### Corrected Version of the Function:
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
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By making the above corrections to handle keys of type `Index` correctly and determine the key type accurately based on the input, the function should now behave as expected and resolve the issue reported on GitHub.