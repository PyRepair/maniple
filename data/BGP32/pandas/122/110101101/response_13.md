### Bug Explanation:
The bug in the `equals` function arises from the sorting of `self.blocks` and `other.blocks` using a custom `canonicalize` function. The `canonicalize` function is supposed to create a tuple with the block's dtype name and `mgr_locs`, but the bug lies in the way `mgr_locs` is converted to a list using `as_array.tolist()`. This conversion is incorrect and leads to comparison failures.

### Bug Fix Strategy:
To fix the bug, we need to correct the `canonicalize` function to properly extract the `mgr_locs` information without causing issues during comparison.

### Corrected Version of the `equals` Function:
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

    # corrected canonicalize function
    def canonicalize(block):
        if isinstance(block, CategoricalBlock):
            return (block.dtype.name, tuple(row.tolist() for row in block.mgr_locs.values))
        else:
            return (block.dtype.name, block.mgr_locs)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By correctly handling the `mgr_locs` extraction in the `canonicalize` function, the corrected version should now pass the failing test and ensure that the blocks are compared properly.