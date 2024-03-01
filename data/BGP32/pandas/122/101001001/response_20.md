### Bug Explanation
The bug in the provided function occurs because the `canonicalize` function incorrectly accesses the `mgr_locs` attribute of the `block` object. The variable `block` is an instance of `IntBlock`, which does not have an attribute `mgr_locs`.

### Bug Fix
To fix the bug, we need to modify the `canonicalize` function to handle `IntBlock` objects correctly. We can change the `canonicalize` function to only consider the `dtype.name` for `IntBlock` objects.

### Corrected Version
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

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        if isinstance(block, IntBlock):
            return (block.dtype.name,)
        else:
            return (block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This corrected version of the function handles the different types of blocks appropriately, ensuring that the bug related to accessing the `mgr_locs` attribute of `IntBlock` objects is resolved.