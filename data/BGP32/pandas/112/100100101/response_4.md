### Bug Explanation
The bug occurs in the `get_indexer` function when dealing with the case where `target_as_index` is an `IntervalIndex`. The current implementation does not handle the case where `target_as_index` has overlapping intervals correctly, resulting in an incorrect return value.

### Bug Location
The issue arises in the check for overlapping indices:
```python
if self.is_overlapping:
    msg = (
        "cannot handle overlapping indices; use "
        "IntervalIndex.get_indexer_non_unique"
    )
    raise InvalidIndexError(msg)
```
This condition is not correctly handling the case of overlapping indices.

### Fix Strategy
To fix the bug, the code needs to be modified to appropriately handle overlapping indices case by implementing logic to correctly handle overlapping intervals.

### Corrected Function
```python
def get_indexer(
    self,
    target: AnyArrayLike,
    method: Optional[str] = None,
    limit: Optional[int] = None,
    tolerance: Optional[Any] = None,
) -> np.ndarray:

    self._check_method(method)

    target_as_index = ensure_index(target)

    if isinstance(target_as_index, IntervalIndex):
        # Equal indexes -> 1:1 positional match
        if self.equals(target_as_index):
            return np.arange(len(self), dtype='intp')

        # Handle overlapping intervals
        if any(s.overlaps(t) for s, t in zip(self, target_as_index)):
            return self.get_indexer_non_unique(target_as_index)
        
        # Handle non-overlapping intervals
        common_subtype = find_common_type(
            [self.dtype.subtype, target_as_index.dtype.subtype]
        )
        if self.closed != target_as_index.closed or is_object_dtype(common_subtype):
            return np.repeat(np.intp(-1), len(target_as_index))

        left_indexer = self.left.get_indexer(target_as_index.left)
        right_indexer = self.right.get_indexer(target_as_index.right)
        indexer = np.where(left_indexer == right_indexer, left_indexer, -1)
    elif not is_object_dtype(target_as_index):
        # Homogeneous scalar index: use IntervalTree
        target_as_index = self._maybe_convert_i8(target_as_index)
        indexer = self._engine.get_indexer(target_as_index.values)
    else:
        # Heterogeneous scalar index: defer elementwise to get_loc
        indexer = []
        for key in target_as_index:
            try:
                loc = self.get_loc(key)
            except KeyError:
                loc = -1
            indexer.append(loc)

    return ensure_platform_int(indexer)
```

In the corrected function, we added logic to handle overlapping intervals correctly by calling `get_indexer_non_unique` when any overlap is detected between the current interval index and the target interval index.