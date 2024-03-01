The bug in the `equals` function arises due to the comparison of blocks' locations without considering their contents. To fix this, we need to ensure that the comparison takes into account the actual data in the blocks. Here's the corrected version of the function:

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

    self_blocks = sorted(self.blocks, key=lambda x: x.values.to_list())
    other_blocks = sorted(other.blocks, key=lambda x: x.values.to_list())
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This corrected version ensures that the blocks are sorted based on their content before comparison, rather than just on their locations. This will correctly handle cases where blocks have the same data but different locations.