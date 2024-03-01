### Bug Explanation
The bug in the `equals` function arises from the comparison of blocks between two `BlockManager` objects. The issue occurs due to the way blocks are sorted and compared. The function sorts the blocks based on the combination of the block's data type name and `mgr_locs`, assuming that this combination uniquely identifies the blocks. However, this approach might not be sufficient for all block types, especially when dealing with unconsolidated blocks (e.g., Categorical blocks).

### Bug Fix Strategy
To fix the bug, we need to ensure that the comparison between blocks is robust and accounts for all block types. One way to achieve this is to enhance the comparison criteria to consider the block's data type and content (e.g., values) instead of relying solely on dtype name and `mgr_locs`.

### Corrected Function
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

    self_blocks = list(self.blocks)
    other_blocks = list(other.blocks)

    if len(self_blocks) != len(other_blocks):
        return False

    for i in range(len(self_blocks)):
        if not self_blocks[i].equals(other_blocks[i]):
            return False
    
    return True
```

The corrected version makes a copy of the blocks in lists for both `self` and `other` instances. It then iterates through each block in both lists, comparing them using the `equals` method of the blocks themselves. This approach ensures a more robust comparison between blocks, encompassing different block types and contents.