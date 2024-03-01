### Bug Explanation
The bug lies in the `canonicalize` function where `block.mgr_locs.as_array.tolist()` is being called. The issue arises because `mgr_locs` is an attribute of the `block`, but it is not being accessed properly. The correct way to access it is `block.mgr_locs` instead of `block.mgr_locs.as_array.tolist()`.

### Bug Fix
To fix the bug, update the `canonicalize` function to only access `block.mgr_locs` without the `as_array.tolist()` calls.

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
        return (block.dtype.name, block.mgr_locs)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```