The issue arises because the `equals` method in the `BlockManager` class is comparing the blocks' locations and types in a way that may lead to incorrect comparisons. The function compares blocks based on their dtype names and mgr_locs, which can be problematic if two identical blocks have different locations.

To fix this issue, we need to modify the `equals` function to compare the blocks based on their values rather than their locations. Here's the corrected version of the `equals` function:

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

    # Check if all blocks are equal in both BlockManagers
    return all(block.values.equals(oblock.values) for block, oblock in zip(self_blocks, other_blocks))
```

In this corrected version, we compare the values of the blocks using the `equals` method. This change ensures that the blocks are compared based on their content rather than their locations. Consequently, the function should now correctly identify if two BlockManagers are equal content-wise.

Please test this corrected function on the failing test case to ensure it passes and resolves the issue reported on GitHub.