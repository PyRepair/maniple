### Bug Explanation:
The bug occurs in the `_get_with` function when handling indexers of different types (list, ndarray, Index, Series). In the case of a list indexer, the function fails to properly handle it, leading to a KeyError when trying to index a Series. The function incorrectly processes the key_type when dealing with list indexers, resulting in an inconsistency with how other indexer types are handled.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the function handles list indexers (and other indexers) consistently and correctly. This can be achieved by updating the logic for processing list indexers to align with the behavior of other types of indexers.

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

    # Handle list indexers consistently
    if is_list_like(key) and not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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
        # Handle duplicate indexers case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

This corrected version ensures that list indexers are correctly processed and handled within the `_get_with` function, addressing the inconsistency and resolving the KeyError issue mentioned in the GitHub problem description.