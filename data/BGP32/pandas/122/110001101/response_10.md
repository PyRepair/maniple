The bug in the function `equals(self, other)` is likely caused by the way the blocks are being compared for equality. The function fails to account for the potential non-consolidated blocks that may exist due to ordering differences. This can lead to incorrect comparison results.

To fix this bug, we need to modify the comparison logic in the function to consider all the aspects that may affect the equality of the blocks, including their dtype and mgr_locs.

Here is the corrected version of the `equals` function:

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
        return (block.get_values().dtype, block.mgr_locs.as_array.tolist())
    
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks))
```

In this corrected version, `canonicalize` function considers block values' dtype and mgr_locs to properly sort and compare the blocks for equality. This should address the issue by accounting for unconsolidated blocks and ordering differences.