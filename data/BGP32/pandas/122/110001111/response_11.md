### Analysis
The `equals` function is meant to compare two `BlockManager` instances for equality based on their axes and blocks. The bug seems to arise from the comparison logic when handling the blocks. The function needs to address the comparison of blocks with different locations.

### Cause of the Bug
The bug occurs in the comparison of `self.blocks` and `other.blocks` where the blocks are sorted by dtype and mgr_locs as a workaround for unconsolidated blocks. However, this sorting method does not consider the actual block values but rather their location and type. This results in wrongly returning `True` when the blocks have the same content but different locations.

### Strategy for Fixing the Bug
To fix the bug, we need to compare the block values themselves instead of their locations. We should iterate over the blocks and compare their content directly to ensure accurate equality checking.

### Corrected Version of the Function
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
    
    def compare_blocks(block1, block2):
        return block1.values.equals(block2.values)
    
    self_blocks = self.blocks
    other_blocks = other.blocks
    
    if len(self_blocks) != len(other_blocks):
        return False
    
    return all(
        compare_blocks(block, oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

This fix introduces the `compare_blocks` function that directly compares the values of the blocks to determine equality. This change ensures that the comparison is based on the actual data within the blocks rather than their locations.