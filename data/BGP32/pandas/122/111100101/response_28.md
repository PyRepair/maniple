### Bug Explanation:
The bug in the `equals` function arises due to the comparison of blocks between two `BlockManager` instances. The bug specifically lies in the `canonicalize` function where it tries to access the `mgr_locs` attribute of the `block` object, which is causing the `AttributeError`.

### Bug Location:
The bug is located within the `canonicalize` function, where `block.mgr_locs` is attempted to be accessed, but `mgr_locs` is not an attribute of the `block` object.

### Bug Fix Strategy:
To fix the bug, we need to revise the logic of how the blocks are sorted and compared within the `equals` function. Instead of trying to access the `mgr_locs` attribute of the blocks directly, we can use a different approach to ensure the blocks are compared correctly.

### Corrected Version:
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

    # canonicalize block order by sorting based on block types
    def canonicalize(block):
        return (type(block).__name__, block.values)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

In the corrected version, the `canonicalize` function now uses the `type` of the block object and its `values` attribute to determine the order for comparison. This modification ensures that the blocks are correctly sorted and compared based on their types, addressing the issue with the original code.