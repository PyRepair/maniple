## Analysis:
1. The `get_indexer` function in the `pandas/core/indexes/interval.py` file is causing an issue when trying to handle overlapping indices.
2. The function is checking if `self.is_overlapping` is `True`, but the logic for handling non-overlapping indices seems to be incorrect.
3. The failing test related to rounding interval category columns in a DataFrame exposes the bug when using CategoricalIndex columns with IntervalIndex values.

## Bug Cause:
The bug occurs in the `get_indexer` function when it tries to handle non-overlapping indices. The logic within the `if` branches for different index types may not be correctly distinguishing the cases. This leads to incorrect results, especially when dealing with heterogeneous scalar indices, causing the function to return unexpected results.

## Fix Strategy:
To fix the bug, we need to revise the logic for handling non-overlapping indices in the `get_indexer` function. Ensure that the code correctly identifies the different cases based on index types and processes them accordingly. Additionally, make sure that the function handles heterogeneous scalar indices properly to prevent incorrect results.

## Code Fix:
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
    elif is_scalar(target_as_index):
        # handle homogeneous scalar index
        target_as_index = self._maybe_convert_i8(target_as_index)
        indexer = self._engine.get_indexer([target_as_index])
    else:
        # handle heterogeneous scalar index
        indexer = np.array([self.get_loc(key) for key in target_as_index], dtype="intp")

    return ensure_platform_int(indexer)
```

This corrected version should address the issue with handling non-overlapping indices correctly and improve the function's overall behavior when dealing with different types of indices.