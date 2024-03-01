The buggy function `get_indexer` within the `IntervalIndex` class seems to have an issue related to the use of the `is_overlapping` attribute.

### Potential Error Location:
The potential error is likely related to the condition check `if self.is_overlapping:`. It may not be correctly handling the case where overlapping indices are detected.

### Bug Explanation:
The bug is likely triggered when the index is overlapping, causing the if condition `if self.is_overlapping:` to evaluate to `True`. This then raises an `InvalidIndexError` with a message about not being able to handle overlapping indices. However, it suggests using `IntervalIndex.get_indexer_non_unique`, which seems to be a non-existent method, leading to a potential bug in the error message logic.

### Solution Strategy:
1. Check the implementation of `is_overlapping` to ensure that it correctly identifies overlapping indices.
2. Modify the error message in `InvalidIndexError` to provide a more informative message or handle the case of overlapping indices appropriately.

### Corrected Version:
Here is the corrected version of the `get_indexer` function:

```python
def get_indexer(
        self,
        target: AnyArrayLike,
        method: Optional[str] = None,
        limit: Optional[int] = None,
        tolerance: Optional[Any] = None,
    ) -> np.ndarray:
    
        self._check_method(method)
        
        # Check if the index is overlapping
        if self.is_overlapping:
            raise NotImplementedError("Overlapping indices are not yet supported.")
        
        target_as_index = ensure_index(target)
        
        if isinstance(target_as_index, IntervalIndex):
            # Implementation for handling IntervalIndex
            # [...]
        elif not is_object_dtype(target_as_index):
            # Implementation for handling scalar index
            # [...]
        else:
            # Implementation for handling heterogeneous scalar index
            # [...]
        
        return ensure_platform_int(indexer)
```

In this corrected implementation:
- The bug related to handling overlapping indices has been fixed by raising a `NotImplementedError` with a clear message.
- The rest of the function's functionality for different index types is preserved.

Please integrate this corrected version into the `IntervalIndex` class to address the bug related to handling overlapping indices.