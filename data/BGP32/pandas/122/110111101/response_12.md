### Bug Explanation
The bug in the `equals` function arises due to the comparison of blocks in an incorrect order. The function sorts both `self_blocks` and `other_blocks` using a custom key function `canonicalize` that combines the block's data type name and `mgr_locs` but doesn't consider the correct order of the blocks.

### Bug Fix Strategy
To fix the bug, we need to ensure that the blocks are sorted in the correct order before comparing them. We should consider the block order based on the `mgr_locs` attribute.

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

    def block_key(block):
        return block.mgr_locs
          
    self_blocks = sorted(self.blocks, key=block_key)
    other_blocks = sorted(other.blocks, key=block_key)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

The corrected version sorts the blocks based on the `mgr_locs` attribute before comparing them, ensuring the correct order for the comparison and fixing the bug.