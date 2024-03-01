### Bug Explanation
The bug in the `equals` function arises from comparing the blocks between `self` and `other` BlockManagers in a faulty manner. The comparison is based on sorting the blocks by their type name and then their memory location, which can lead to incorrect results. In the failing test case, `df1` and `df2` have the same columns ('a' and 'b') but with different data types and are in reverse order.

### Bug Fix Strategy
To fix the bug in the `equals` function, we need to modify the comparison of blocks to ensure that we are comparing the actual data instead of relying on type names and memory locations. We should compare the values within the blocks themselves rather than their type names. 

### Corrected Version of the `equals` Function
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
    if len(self_blocks) != len(other_blocks):
        return False

    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By comparing the actual block data in `self_blocks` and `other_blocks`, rather than relying on their type names and memory locations, the corrected `equals` function should now pass the failing test case and resolve the issue reported on GitHub.