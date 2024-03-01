### Cause of the Bug
The bug is caused by the incorrect comparison of blocks in the `equals` function of the `BlockManager` class. The function sorts the blocks using a custom `canonicalize` function that combines the block's data type name and manager locations, but it fails to account for the fact that the `mgr_locs` attribute itself should be set by the `_consolidate_inplace` method, ensuring consistent comparison.

### Strategy for Fixing the Bug
To fix the bug, the `canonicalize` function that sorts the blocks should include the comparison of `mgr_locs` values, ensuring that the blocks are first consolidated before being compared. This ensures that unconsolidated blocks with different locations are correctly distinguished when checking for equality.

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

    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

In the corrected version, the `canonicalize` function now correctly incorporates the `mgr_locs()` of each block for comparison. This change ensures that before comparing the blocks, they are suitably consolidated, allowing for accurate check of equality based on both data type and block locations.