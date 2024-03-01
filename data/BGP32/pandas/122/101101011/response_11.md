### Analysis:
- The buggy function `equals` in the `BlockManager` class is attempting to compare two `BlockManager` instances based on their axes and blocks.
- The function iterates over the axes of `self` and `other` to check if each axis is equal, then consolidates both instances, sorts the blocks based on type and locations, and finally compares each block.
- The bug is causing the function to return True even when the `BlockManager` instances have identical blocks with different locations, leading to incorrect behavior.
- The failing test `test_dataframe_not_equal` demonstrates this bug by creating two `DataFrame` instances with columns swapped and expecting `equals` to return False, but it incorrectly returns True.

### Bug Cause:
- The bug arises from the `canonicalize` function used to sort the blocks based on type and locations. The sorting by `mgr_locs` can cause identical blocks with different locations to be considered equal, leading to incorrect comparison.

### Fix Strategy:
- We need to modify the `canonicalize` function to exclude `mgr_locs` from the criteria to ensure that blocks with different locations are not considered equal.
- The comparison logic should focus on the data within the blocks rather than their locations.

### Corrected Version:
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

    def canonicalize(block):
        return block.dtype.name

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

After making the above changes, the `equals` function should now correctly compare two `BlockManager` instances based on their blocks' data content only, without considering their locations. This correction should address the issue reported on GitHub and make the failing test `test_dataframe_not_equal` pass.