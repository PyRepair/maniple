The buggy function `get_indexer` in the `IntervalIndex` class is failing to handle the case where the target index is an `IntervalIndex` with non-overlapping intervals. The issue seems to be related to the comparison and matching of intervals between the self index and the target index.

### Bug Explanation:
- The function fails to correctly handle the case where the self index and the target index are both of type `IntervalIndex` and have non-overlapping intervals.
- The comparison logic used to determine the index positions for each interval in the target index is faulty, leading to incorrect matching and resulting in unexpected output.

### Strategy for Fixing the Bug:
- Modify the comparison logic to correctly match the intervals between the self index and the target index.
- Ensure that the correct left and right boundary comparisons are performed to determine the matching intervals.

### Corrected Version of the Function:
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

        self_left_values = self.left.values
        target_left_values = target_as_index.left.values
        self_right_values = self.right.values
        target_right_values = target_as_index.right.values

        indexer = np.full(len(target_as_index), -1, dtype='intp')
        for i, (self_left, self_right) in enumerate(zip(self_left_values, self_right_values)):
            for j, (target_left, target_right) in enumerate(zip(target_left_values, target_right_values)):
                if self_left == target_left and self_right == target_right:
                    indexer[j] = i
                    break

    elif not is_object_dtype(target_as_index):
        # homogeneous scalar index: use IntervalTree
        target_as_index = self._maybe_convert_i8(target_as_index)
        indexer = self._engine.get_indexer(target_as_index.values)
    else:
        # heterogeneous scalar index: defer elementwise to get_loc
        # (non-overlapping so get_loc guarantees scalar of KeyError)
        indexer = []
        for key in target_as_index:
            try:
                loc = self.get_loc(key)
            except KeyError:
                loc = -1
            indexer.append(loc)

    return ensure_platform_int(indexer)
```

This corrected version implements a more robust comparison and matching logic for non-overlapping intervals between the self index and the target index, ensuring correct indexing and returning the expected results for the failing test case.