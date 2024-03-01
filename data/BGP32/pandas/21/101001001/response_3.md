## Bug Explanation
The bug in the `_get_with` function is related to how different types of `key` are handled. The function is designed to process different types of keys, such as slices, tuples, lists, DataFrames, etc. However, there is a problem in the logic for handling non-list-like and non-Index key types.

In the cases provided:
- Case 1: The key type is a list, but the key is wrongly categorized as a string due to the faulty logic in the function.
- Case 2: The key type is an ndarray, but again, it's misinterpreted as a string.
- Case 3: The key type is an Index, and the inference for key_type is correct.
- Case 4: The key type is a Series, but it's identified wrongly as a string.

The incorrect classification of key types as strings leads to improper processing in the subsequent steps, impacting the returned result.

## Bug Fix Strategy
To fix the bug, we need to ensure that the key type is correctly identified and processed. We should account for all possible types that `key` can have and handle each case appropriately without misinterpreting the key type.

## Corrected Version of the Function
Below is the corrected version of the `_get_with` function:

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

    if is_scalar(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = lib.infer_dtype(key, skipna=False)
        
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]

        return self.reindex(key)
```

In the corrected version:
- The function now correctly handles scalars as non-list-like key types.
- It properly determines the key type and infers whether it's an integer or other types to take the appropriate action.
- The bugs related to misinterpreting the key type have been resolved, leading to more accurate processing of different key types.