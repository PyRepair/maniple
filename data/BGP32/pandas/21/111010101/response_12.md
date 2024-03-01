### Analysis
1. The buggy function `_get_with` is responsible for handling different types of keys when indexing a Series. It checks the type of the key and then processes it accordingly.
2. The failing test cases are related to indexing a Series with keys of different types (`list`, `ndarray`, `Index`, `Series`) which should raise a `KeyError` when none of the keys match the index.
3. The bug seems to be related to how the function handles the different key types and determines the `key_type`.
4. The key type should be correctly inferred based on the type of the key.
5. The fix should ensure that the `key_type` is inferred accurately and the correct branch of the conditional statements is chosen based on the key type.

### Bug
The bug in the `_get_with` function is related to the incorrect inference of the `key_type` when dealing with different types of keys. This leads to incorrect branching in the key handling logic, resulting in incorrect indexing and the `KeyError` not being raised as expected when none of the keys are found in the index.

### Fix
To fix the bug, we need to ensure that the `key_type` is inferred accurately based on the type of the key. Then we need to correctly handle the different cases of keys such as `'integer'`, `'list'`, and others. We can update the logic to handle key types correctly and raise `KeyError` when none of the keys are present in the index.

### Corrected Version
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

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

    if isinstance(key, list) or isinstance(key, np.ndarray):
        return self.loc[key]

    raise KeyError(f"None of {key} are in the index")
``` 

This corrected version of the `_get_with` function accurately infers the `key_type` based on the type of the key and correctly handles different cases of keys to ensure that a `KeyError` is raised when none of the keys are found in the index.