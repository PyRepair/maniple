## Bug Analysis
The `equals` function in the `BlockManager` class is intended to compare two `BlockManager` objects for equality based on their axes and blocks. The bug seems to be related to the comparison of blocks in the `self` and `other` `BlockManager` instances. The issue on GitHub indicates that the function wrongly returns `True` when comparing identical blocks with different locations.

## Bug Location
The bug seems to be related to how the `self_blocks` and `other_blocks` are sorted and compared in the function. The comparison is being done based on the sorted blocks, but the bug arises when the actual locations of the blocks should also be considered for a valid comparison.

## Bug Cause
The bug is caused because the function is comparing blocks based on type name and manager locations, without considering the actual content of the blocks. This leads to cases where blocks with identical contents but different locations are treated as unequal.

## Fix Strategy
To fix the bug, we need to compare the actual content of the blocks instead of just their types and manager locations. This can be achieved by comparing the values of the blocks directly when checking for equality.

## Corrected Version
Here is the corrected version of the `equals` function:

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
    
    self_blocks = self.blocks
    other_blocks = other.blocks
    
    return all(
        block.values.equals(oblock.values) for block, oblock in zip(self_blocks, other_blocks)
    )
```

In this corrected version, we compare the values of the blocks directly using the `equals` method of the block values. This ensures that the comparison is based on the actual content of the blocks rather than just their types and locations. This should address the issue reported on GitHub.