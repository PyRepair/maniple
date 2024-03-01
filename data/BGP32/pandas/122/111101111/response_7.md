### Bug Explanation:
The `equals` function in the `BlockManager` class is incorrectly comparing the blocks in a non-standard order, leading to false positives even when the blocks are not equal. The comparison is done after sorting the blocks based on the block type name and `mgr_locs`. This can cause blocks with the same content but different locations to be considered equal.

### Fix Strategy:
To fix this bug, we should modify the comparison logic to ensure that blocks are compared based on their contents rather than their order or location.

### Corrected Version of the `equals` Function:
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

    self_blocks = sorted(self.blocks, key=lambda block: id(block))
    other_blocks = sorted(other.blocks, key=lambda block: id(block))
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By sorting the blocks based on their identifiers (`id(block)`) rather than their type and location, we ensure that the comparison is made based on the content of the blocks. This correction should address the issue reported in the GitHub bug and correctly identify cases where blocks are different despite similar types and locations.