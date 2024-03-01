### Bug Explanation
The bug in the provided function arises due to the comparison of blocks in different orders. The function attempts to sort the blocks based on their dtype name and mgr_locs, but the comparison breaks down when the blocks are unconsolidated. This leads to incorrect results in certain cases where the blocks are not consolidating in the same order, even though they are equivalent.

### Bug Fix Strategy
To fix the bug, we need to determine a consistent and accurate way to compare the blocks regardless of their consolidation state. One approach could be to compare each block in `self.blocks` with every block in `other.blocks` to ensure all equivalent blocks are compared, hence ensuring correctness.

### Corrected Version
```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes):
        return False
    if not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False

    self_blocks = self.blocks
    other_blocks = other.blocks
    
    if len(self_blocks) != len(other_blocks):
        return False
    
    def equal_blocks(block1, block2):
        return block1.equals(block2)
    
    # Compare each block in self.blocks with each block in other.blocks
    for block1 in self_blocks:
        found_equal_block = False
        for block2 in other_blocks:
            if equal_blocks(block1, block2):
                found_equal_block = True
                break
        if not found_equal_block:
            return False
    
    return True
```

This corrected version ensures that each block in `self.blocks` is compared with every block in `other.blocks` to accurately determine their equality, addressing the bug present in the original function.