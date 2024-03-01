### Bug Explanation

The bug in the `_get_with` function arises from how the function handles the input `key`. The function checks the type of `key` and then tries to determine the type of values inside `key` to decide how to index the Series. In the failing test cases, the input `key` is of type `ndarray`, `Index`, or `Series`, and the function incorrectly identifies the `key_type` as `'string'`. This misidentification leads to incorrect indexing operations, causing the test to fail with a `KeyError`.

### Bug Fix Strategy

To fix the bug, we need to correctly identify the type of the `key` and handle different types accordingly. Specifically, we should correctly identify the type of values inside the `key` and decide whether to treat it as a positional indexer (using `iloc`) or label-based (using `loc`). Additionally, for certain types like `Index`, we need to extract the inferred type correctly.

### Corrected Code

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

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        elif isinstance(key, list):
            return self.loc[key]

    return self.reindex(key)
```

This corrected version of the function correctly identifies the type of `key` and handles different types appropriately, ensuring that the indexing operations are performed correctly. After making these changes, the function should pass the failing test cases.