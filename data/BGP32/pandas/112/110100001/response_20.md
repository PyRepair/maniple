The bug in the `get_indexer` function of the `IntervalIndex` class is related to handling non-overlapping indices, where it tries to compare left and right intervals for exact matches. However, the implementation does not correctly handle the comparison logic resulting in incorrect indexing.

To fix this bug, we need to adjust the logic for comparing left and right intervals to determine the correct indexer position. The corrected version of the `get_indexer` function is provided below:

```python
    def get_indexer(
        self,
        target: AnyArrayLike,
        method: Optional[str] = None,
        limit: Optional[int] = None,
        tolerance: Optional[Any] = None,
    ) -> np.ndarray:
        self._check_method(method)
    
        if self.is_overlapping:
            msg = (
                "cannot handle overlapping indices; use "
                "IntervalIndex.get_indexer_non_unique"
            )
            raise InvalidIndexError(msg)
    
        target_as_index = ensure_index(target)
    
        if isinstance(target_as_index, IntervalIndex):
            # equal indexes -> 1:1 positional match
            if self.equals(target_as_index):
                return np.arange(len(self), dtype="intp")
    
            # different closed or incompatible subtype -> no matches
            common_subtype = find_common_type(
                [self.dtype.subtype, target_as_index.dtype.subtype]
            )
            if self.closed != target_as_index.closed or is_object_dtype(common_subtype):
                return np.repeat(np.intp(-1), len(target_as_index))
    
            # non-overlapping -> at most one match per interval in target_as_index
            # want exact matches -> need both left/right to match, so defer to
            # left/right get_indexer, compare elementwise, equality -> match
            left_indexer = self.left.get_indexer(target_as_index.left)
            right_indexer = self.right.get_indexer(target_as_index.right)
    
            indexer = np.where(left_indexer == right_indexer, left_indexer, -1)
        else:
            indexer = target_as_index.get_indexer(self)
    
        return ensure_platform_int(indexer)
```

By comparing the left and right intervals correctly and using the appropriate logic for non-overlapping indices, the corrected function should pass the failing test provided.