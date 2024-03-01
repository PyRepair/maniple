### Analysis:
1. The buggy function `get_indexer` within the `IntervalIndex` class is responsible for the bug related to rounding when the columns are `CategoricalIndex` created from an `IntervalIndex`.
2. The function checks for overlapping indices and raises an `InvalidIndexError` if overlapping indices are detected.
3. The bug occurs when the function encounters an `IntervalIndex` type in the target data. It fails to handle the scenario where the target data is a homogeneous scalar index.
4. The failure to handle the homogeneous scalar index case leads to a mismatch in data types and causes the rounding method to fail, resulting in a `TypeError`.
5. To fix the bug, we need to modify the logic in the `get_indexer` function to properly handle the case of a homogeneous scalar index.

### Bug Fix:
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
            if self.equals(target_as_index):
                return np.arange(len(self), dtype="intp")
            common_subtype = find_common_type(
                [self.dtype.subtype, target_as_index.dtype.subtype]
            )
            if self.closed != target_as_index.closed or is_object_dtype(common_subtype):
                return np.repeat(np.intp(-1), len(target_as_index))

            left_indexer = self.left.get_indexer(target_as_index.left)
            right_indexer = self.right.get_indexer(target_as_index.right)
            indexer = np.where(left_indexer == right_indexer, left_indexer, -1)
        else:
            indexer = []
            for key in target_as_index:
                try:
                    loc = self.get_loc(key)
                    indexer.append(loc)
                except KeyError:
                    indexer.append(-1)
    
        return ensure_platform_int(indexer)
```

### Explanation of Fix:
- Modified the logic to handle the case when the target data is not an `IntervalIndex` but a homogeneous scalar index, by iterating over the target data and using `get_loc` method to retrieve the index.
- Added a try-except block to catch `KeyError` exceptions when calling `get_loc`.
- Appended the retrieved location to the `indexer` list in case of successful retrieval or -1 otherwise for missing keys.
- This modification ensures that the function handles the scenario of a homogeneous scalar index properly and provides the correct indexer array for further operations like rounding.

By applying this fix, the `get_indexer` function will correctly handle the situation where columns are `CategoricalIndex` created from an `IntervalIndex`, resolving the rounding issue reported in the GitHub issue.