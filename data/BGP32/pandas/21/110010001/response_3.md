### Analysis:
The function `_get_with` is responsible for handling different types of keys when indexing a `Series` object. The bug seems to occur when dealing with cases involving a `key` that is not recognized as list-like.

### Potential Error Locations:
1. The conditional check for non-list-like keys may not cover all cases correctly.
2. The conversion of the key to a list in the function could be causing unexpected behavior.
3. Handling of Index objects and their inferred types might have issues.

### Cause of the Bug:
The error message implies that the code fails to raise a `KeyError` when attempting to index with certain key types. It seems like the logic for handling non-list-like keys might be flawed, leading to unexpected behavior.

### Bug Fix Strategy:
To fix this bug, we need to ensure that all key types are properly handled according to the expected behavior. Specifically, we should pay attention to how non-list-like keys are processed and make sure that the indexing operation raises a `KeyError` when a key is not present in the index.

### Corrected Version:
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

    if is_list_like(key):
        key = list(key)
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    # Use isinstance checks instead of 'key_type' comparison for better handling
    if isinstance(key, (int, np.int32, np.int64)):
        key = [key]
    elif isinstance(key, float):
        return self.loc[key]  # Return loc for floating-point keys, adjust if needed
    elif isinstance(key, str):
        return self.loc[key]  # Return loc for string keys, adjust if needed

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version handles different types of keys more adaptively and ensures that non-list-like keys are properly processed. Make sure to test this corrected function with the failing test cases to verify the bug fix.