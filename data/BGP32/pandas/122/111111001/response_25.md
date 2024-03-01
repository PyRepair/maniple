### Bug Explanation
The bug in the `equals` function arises due to the comparison between `self.blocks` and `other.blocks`. The comparison logic is incorrect because `self.blocks` and `other.blocks` are tuples containing block types as keys and block details as values. The current approach to sorting and comparing these tuples based on block types is flawed and leads to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to modify the method of comparing the blocks within `self.blocks` and `other.blocks`. Instead of relying on sorting based on block types, we should compare blocks directly based on their content by iterating over the blocks in both sets.

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

    self_blocks = self.blocks
    other_blocks = other.blocks

    if len(self_blocks) != len(other_blocks):
        return False

    for self_block, other_block in zip(self_blocks, other_blocks):
        if not self_block.equals(other_block):
            return False

    return True
```

With this corrected version of the `equals` function, it should now properly compare the blocks within `self.blocks` and `other.blocks` based on their content rather than their types. It should resolve the issue identified in the failing test.