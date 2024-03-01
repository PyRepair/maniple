### Bug Explanation
The bug in the `equals` function arises from the `canonicalize` function. The `canonicalize` function is attempting to create a tuple to compare blocks based on their type name and memory locations. However, the `block.dtype.name` is used directly without converting it to a string. This causes an error when trying to concatenate it with `block.mgr_locs.as_array.tolist()` in the tuple creation.

### Bug Fix
To fix the bug, we should convert the `block.dtype.name` to a string before using it in the tuple. 

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
        return (str(block.dtype.name), block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```