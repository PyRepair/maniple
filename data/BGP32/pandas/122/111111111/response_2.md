### Bug Explanation:
The bug in the `equals` function arises from the comparison of `self.blocks` and `other.blocks`. The comparison logic uses the `sorted` function which sorts the blocks based on their dtype name and manager locations. However, the comparison of `block.equals(oblock)` inside the `all()` function is using the original blocks which may not be in the correct order due to sorting. This discrepancy in ordering results in the `equals` function incorrectly returning `True` instead of `False`.

### Fix Strategy:
To fix the bug, we need to ensure that the comparison between blocks is done based on the sorted order of blocks from both `self` and `other`. This involves sorting the blocks based on the dtype name and manager locations before performing the comparison.

### Corrected Version of the `equals` function:
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

    # sort blocks based on dtype name and manager locations
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    # compare blocks in sorted order
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

With this corrected version, the `equals` function should now correctly compare the blocks from `self` and `other` in a sorted manner, resolving the issue with the failing test.