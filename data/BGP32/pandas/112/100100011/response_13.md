### Analysis:
1. The `get_indexer` function from the `pandas.core.indexes.interval` file is responsible for finding the indices of values in an IntervalIndex.
2. The failing test is related to rounding values in a DataFrame with a CategoricalIndex of IntervalIndex columns.
3. The bug causes a `TypeError: No matching signature found` when calling the `round` method on a DataFrame with CategoricalIndex columns of IntervalIndex values.
4. The bug arises because the `get_indexer` function does not handle the case when the target index is a CategoricalIndex instead of an IntervalIndex.
   
### Bug Fix Strategy:
1. Adjust the get_indexer function to handle the case when the target index is a CategoricalIndex.
2. Modify the logic to support rounding for CategoricalIndex columns of IntervalIndex values.

### Updated/Copy-paste Corrected Version of the `get_indexer` Function:

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

    if isinstance(target_as_index, (IntervalIndex, CategoricalIndex)):
        if isinstance(target_as_index, CategoricalIndex):
            if isinstance(target_as_index._index, IntervalIndex):
                target_as_index = target_as_index._index
            else:
                raise NotImplementedError(
                    "Handling CategoricalIndex with non-IntervalIndex values is not implemented"
                )

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

After applying this corrected version, the `round_interval_category_columns` test should pass without any errors.