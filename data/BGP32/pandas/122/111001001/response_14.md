### Bug Explanation:
The bug in the `equals` function is likely due to the way blocks are compared during the final check. The sorting based on block type and locations might not be effective in comparing blocks since the block object itself is not being compared properly.

### Bug Fix:
To fix the bug, we need to ensure that the equality check of blocks is done correctly. We should compare the blocks directly instead of relying on sorting based on dtype and mgr_locs. 

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
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

In this corrected version, we compare the blocks directly using the `equals` method of the block objects themselves, ensuring a proper comparison.

This should fix the bug in the `equals` function.