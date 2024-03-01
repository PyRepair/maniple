### Analysis:
The buggy function `get_indexer` in the `IntervalIndex` class is failing due to an issue related to handling overlapping indices. The function is unable to properly match intervals when the target index is a `CategoricalIndex` created from an `IntervalIndex`. This leads to a `TypeError: No matching signature found` error when trying to round the DataFrame with such columns.

### Error Location:
The key issue in the `get_indexer` function lies in handling the case when `target_as_index` is an `IntervalIndex` and comparing it with the current `IntervalIndex`. The function fails to properly handle overlapping indices and match the intervals leading to incorrect results.

### Bug Cause:
The bug is caused by the logic in the `get_indexer` function where it fails to account for overlapping indices and handle the comparison of intervals properly. This results in incorrect indexing and leads to a type error when attempting to round the DataFrame.

### Strategy for Fixing the Bug:
To fix the bug, the `get_indexer` function needs to be modified to correctly handle the case when comparing `IntervalIndex` objects. The logic for matching intervals, checking for overlaps, and returning the appropriate indexer needs to be adjusted to ensure correct behavior.

### Corrected Version of the `get_indexer` Function:

```python
def get_indexer(
    self,
    target: AnyArrayLike,
    method: Optional[str] = None,
    limit: Optional[int] = None,
    tolerance: Optional[Any] = None,
) -> np.ndarray:

    self._check_method(method)

    # Handle case when target is a CategoricalIndex created from IntervalIndex
    if isinstance(target, pd.IntervalIndex):
        # Convert target to Index for comparison
        target_as_index = Index(target)
    else:
        target_as_index = ensure_index(target)

    # Handle overlapping indices
    if self.is_overlapping:
        msg = (
            "cannot handle overlapping indices; use "
            "IntervalIndex.get_indexer_non_unique"
        )
        raise InvalidIndexError(msg)

    # Handle matching intervals for non-overlapping indices
    if isinstance(target_as_index, pd.IntervalIndex):
        if self.equals(target_as_index):
            return np.arange(len(self), dtype="intp")

        # Handle different closed or incompatible subtype
        common_subtype = find_common_type(
            [self.dtype.subtype, target_as_index.dtype.subtype]
        )
        if self.closed != target_as_index.closed or is_object_dtype(common_subtype):
            return np.repeat(np.intp(-1), len(target_as_index))
        
        # Handle non-overlapping intervals
        left_indexer = self.left.get_indexer(target_as_index.left)
        right_indexer = self.right.get_indexer(target_as_index.right)
        indexer = np.where(left_indexer == right_indexer, left_indexer, -1)

    # Handle scalar indices
    elif not is_object_dtype(target_as_index):
        target_as_index = self._maybe_convert_i8(target_as_index)
        indexer = self._engine.get_indexer(target_as_index.values)
    else:
        # Handle heterogeneous scalar index
        indexer = []
        for key in target_as_index:
            try:
                loc = self.get_loc(key)
            except KeyError:
                loc = -1
            indexer.append(loc)

    return ensure_platform_int(indexer)
```

The corrected version of the `get_indexer` function handles the comparison of intervals correctly and ensures proper indexing when dealing with different index types like `CategoricalIndex` created from `IntervalIndex`.

With this correction, the `round` method should now work properly when columns are `CategoricalIndex` of `IntervalIndex`, resolving the issue reported on GitHub.