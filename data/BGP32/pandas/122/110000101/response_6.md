### Bug Explanation
The buggy function `equals` is not properly comparing the `blocks` attribute of two `BlockManager` instances. The comparison logic is correct, but there are issues with the data preparation for the comparison.

1. The `self_axes` and `other_axes` are correctly extracted from the `BlockManager` instances, but the comparison logic is flawed.
2. The `self._consolidate_inplace()` and `other._consolidate_inplace()` methods are called to consolidate the blocks, but the return value is not assigned back to `self` and `other`.
3. The `canonicalize` function is not correctly considering the block's `mgr_locs` attribute, leading to incorrect sorting of blocks.

### Strategy for Fixing the Bug
1. Ensure that the comparison of `self_axes` and `other_axes` is correctly implemented.
2. Assign the results of `_consolidate_inplace()` back to `self` and `other`.
3. Modify the `canonicalize` function to properly consider the `mgr_locs` attribute of the blocks.

### Corrected Version of the Function
```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes):
        return False
    if not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False
    self = self._consolidate_inplace()
    other = other._consolidate_inplace()
    if len(self.blocks) != len(other.blocks):
        return False

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.__repr__())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

### Changes Made
1. Assign the results of `_consolidate_inplace()` back to `self` and `other`.
2. Modified the `canonicalize` function to consider `mgr_locs` correctly.

By making these changes, the function should now correctly compare the `BlockManager` instances based on the specified criteria.