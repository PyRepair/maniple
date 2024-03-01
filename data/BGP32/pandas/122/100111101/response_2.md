### Bug Explanation
The bug in the `equals` function arises from comparing the blocks in `self` and `other` DataFrames without taking into account the correct order of the columns. The function sorts the blocks based on a `(dtype.name, mgr_locs)` tuple to canonicalize them, but this is incorrect for DataFrames with mismatched column values.

The failing test `test_dataframe_not_equal` creates two DataFrames `df1` and `df2` with columns swapped. The function sorts the blocks in `self` and `other` based on the dtype and mgr_locs, leading to incorrect comparisons and returning `True` instead of `False`.

### Fix Strategy
To fix this bug, we need to modify how the function compares the blocks of `self` and `other` DataFrames. Instead of sorting and comparing based on dtype and mgr_locs, we should directly compare the columns of blocks.

### Corrected Version
```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes):
        return False
    if not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False
    self._consolidate_inplace()
    other._consolidate_inplace()
    if len(self.blocks) != len(other.blocks):
        return False

    return all(
        all(block1.equals(block2) for block1, block2 in zip(blocks1, blocks2))
        for blocks1, blocks2 in zip(self.blocks, other.blocks)
    )
```

In the corrected version, we directly compare each block in `self.blocks` with the corresponding block in `other.blocks`, ensuring a proper comparison of columns. This change addresses the issue in the original function and should make the failing test `test_dataframe_not_equal` pass as expected.