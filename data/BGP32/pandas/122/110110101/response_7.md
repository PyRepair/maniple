### Bug Explanation
The buggy function `equals` is intended to compare two `BlockManager` objects in a way that considers their axes and blocks. The bug occurs due to the incorrect comparison logic. The function is comparing the blocks based on their ordered type name and `mgr_locs` values, but this logic is flawed because the blocks might not be consolidated, leading to wrong comparison results.

### Bug Fix Strategy
To fix the bug, we need to ensure that both `BlockManager` objects are consolidated before proceeding with the block comparison. This consolidation will guarantee that blocks are in a consistent state for comparison.

### Corrected Function
```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes) or not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False
    
    self._consolidate_inplace()
    other._consolidate_inplace()
    
    if len(self.blocks) != len(other.blocks):
        return False
    
    # Compare consolidated blocks
    self_blocks = self.blocks
    other_blocks = other.blocks
    
    return all(
        block.equals(oblock)
        for block, oblock in zip(self_blocks, other_blocks)
    )
```

By ensuring both `BlockManager` objects are consolidated before comparing the blocks, this corrected function should pass the failing test case.