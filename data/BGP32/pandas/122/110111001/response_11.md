### Bug Explanation:
The `equals` function in the `BlockManager` class is comparing two instances of `BlockManager`. The bug lies in the comparison of blocks within these instances. The issue arises because during the block comparison, the ordering of blocks can influence the outcome due to the unconsolidated blocks, such as `Categorical` blocks. 

The bug causes the `equals` function to return `False` even when the underlying data in both `BlockManager` instances is the same.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the comparison of blocks in `self` and `other` `BlockManager` instances considers the data within the blocks rather than relying on their ordering. One way to achieve this is by comparing the block values instead of just sorting and comparing the blocks based on type names.

### Corrected Version of the `equals` Function:
Here is the corrected version of the `equals` function in the `BlockManager` class:

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

    self_blocks = dict((block.mgr_locs, block.values) for block in self.blocks)
    other_blocks = dict((block.mgr_locs, block.values) for block in other.blocks)

    return self_blocks == other_blocks
```

This corrected version compares the block values stored in dictionaries based on their manager locations, ensuring a proper comparison of block data.