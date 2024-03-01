### Bug Explanation
The bug in the `equals` function arises from the fact that the `canonicalize` function is attempting to use the `mgr_locs` attribute of the `block` object, but it incorrectly refers to it as a method `as_array`. This leads to the error in converting the `mgr_locs` to a list and comparing the blocks for equality.

### Fix Strategy
To resolve the bug, we need to change the `_consolidate_inplace` method to actually consolidate the blocks. Then, in the `canonicalize` function, we need to access the `mgr_locs` attribute directly to create a tuple that combines the block's type name and location information.

### Corrected Version of the Buggy Function
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
        return (type(block).__name__, block.mgr_locs)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

The corrected version addresses the issue by correctly accessing the `mgr_locs` attribute in the `canonicalize` function. This modification ensures that the block comparison for equality is performed accurately.