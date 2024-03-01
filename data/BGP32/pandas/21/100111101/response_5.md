## Bug Analysis
The buggy function `_get_with` contains a bug that causes it to incorrectly handle the input when the key is a list-like object (array, Index, Series) with no matching values in the Series index. The function incorrectly infers the key type as `'string'`, leading to an incorrect path in the control flow that ultimately results in the function not raising a `KeyError`, as expected by the test cases.

## Bug Explanation
The bug arises from the incorrect inference of the key type in the cases where the key is a list, ndarray, Index, or Series. The function incorrectly infers the key type as `'string'`, which skips the expected exception-raising block of code where a `KeyError` should be raised when the key has no matching values in the Series index.

The function then goes on to try to reindex the Series with the provided key, which diverges from the expected behavior causing the test to fail.

## Bug Fix Strategy
To fix this bug, we need to correctly infer the key type when the key is a list, ndarray, Index, or Series. This correct inference will ensure that the function takes the appropriate path to raise a `KeyError` when there are no matching values in the Series index.

Let's modify the function to correctly determine the key type and then handle the case where no matching values are found by raising a `KeyError` as expected by the failing tests.

## Corrected Version of the Function
```python
def _get_with(self, key):
    # Implementation for handling list-like objects with no matching values
    if is_list_like(key):
        if key.size == 0 or np.in1d(key, self.index).sum() == 0:
            raise KeyError(f"None of {key} are in the index")
    
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

With this corrected version of the function, the `_get_with` function will now correctly handle the case where a list-like object with no matching values is passed as the key and will raise a `KeyError` as expected by the failing tests.