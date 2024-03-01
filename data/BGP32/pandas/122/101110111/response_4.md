### Bug Explanation
The bug in the `equals` function arises from comparing blocks within the `BlockManager` instance. The issue occurs because the blocks are being sorted using a tuple combining the type name and `mgr_locs`, which might lead to incorrect results when comparing blocks with the same type but different locations.

### Bug Fix Strategy
To fix the bug, we should update the `canonicalize` function used for sorting the blocks. Instead of solely relying on the type name and `mgr_locs`, we should consider the block values as well to ensure a proper comparison. This adjustment will prevent the comparison issue related to blocks with the same type but different locations.

### Corrected Version of the `equals` function
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
        return (block.values, block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By including the `block.values` in the `canonicalize` function, we ensure that block values are considered when sorting the blocks, which should lead to correct comparisons and resolve the bug reported in the GitHub issue.