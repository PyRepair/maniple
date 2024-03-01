### Bug Explanation
The `equals` function is comparing the `self` and `other` block managers by first checking if the axes are equal, then consolidating both managers, and finally comparing the blocks' equality in a sorted order. However, there is a bug in how the blocks are being sorted for comparison. The bug occurs because the `block` objects are sorted based on a tuple of their `dtype.name` and `mgr_locs`, but the attribute `mgr_locs` is used incorrectly in the `canonicalize` function. 

### Bug Fix Strategy
To fix the bug, we need to modify the `canonicalize` function to correctly retrieve the `mgr_locs` attribute as a list. This will ensure that the blocks are sorted based on the correct information for comparison.

### Corrected Version of the `equals` Function
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
        return (block.dtype.name, block.mgr_locs.get_locs())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By correctly retrieving the locations of the blocks using `mgr_locs.get_locs()`, we ensure that the blocks are compared based on their actual locations, resolving the bug in the `equals` function.