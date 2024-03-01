After analyzing the buggy function `get_indexer` and the failing test related to rounding interval category columns, it seems that the bug occurs when trying to round a DataFrame with a CategoricalIndex of IntervalIndex columns. The issue seems to stem from the implementation of the `get_indexer` function in the `pandas/core/indexes/interval.py` file.

The bug appears to be related to how the function handles the case when the target is an `IntervalIndex` and when the target is a CategoricalIndex made from an `IntervalIndex`. The current implementation of the function does not consider this scenario properly, leading to a `TypeError: No matching signature found` when trying to round the DataFrame with CategoricalIndex columns.

To fix this bug:
- We need to modify the logic in the `get_indexer` function to handle the case of CategoricalIndex made from an IntervalIndex correctly.
- Specifically, we should ensure that when the target is a CategoricalIndex, the function should extract the underlying IntervalIndex and handle it accordingly in the rounding process.

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

    if isinstance(target_as_index, CategoricalIndex):
        target_as_index = target_as_index.categories  # Extract the underlying IntervalIndex
        common_subtype = find_common_type(
            [self.dtype.subtype, target_as_index.dtype.subtype]
        )
        if self.closed != target_as_index.closed or is_object_dtype(common_subtype):
            return np.repeat(np.intp(-1), len(target_as_index))

    if isinstance(target_as_index, IntervalIndex):
        # Handle IntervalIndex as before
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

    elif not is_object_dtype(target_as_index):
        target_as_index = self._maybe_convert_i8(target_as_index)
        indexer = self._engine.get_indexer(target_as_index.values)
    else:
        indexer = []
        for key in target_as_index:
            try:
                loc = self.get_loc(key)
            except KeyError:
                loc = -1
            indexer.append(loc)

    return ensure_platform_int(indexer)
```

This corrected version of the `get_indexer` function should address the issue of rounding when the columns are a CategoricalIndex of IntervalIndex type, as described in the GitHub issue.