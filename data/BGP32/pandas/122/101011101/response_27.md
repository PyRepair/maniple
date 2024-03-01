### Bug Explanation
The bug in the `equals` function arises because the function `canonicalize` is used to sort the blocks based on the block's dtype name and `mgr_locs`. The issue is that `mgr_locs` is not a property of the `Block` object but a property of `BlockPlacement` object. This causes an AttributeError when trying to access `mgr_locs`.

### Bug Fix Strategy
To fix the bug, we need to modify the `canonicalize` function to handle the `Block` objects correctly by extracting relevant information from the blocks that can be used for comparison. We should avoid trying to access `mgr_locs` directly from the `Block` object.

### Corrected Version of the Function
Here is the corrected version of the `equals` function:

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
        return block.values.tostring()

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This corrected version retrieves the block's values and converts them to a string for comparison in the `canonicalize` function. Therefore, the function can now correctly compare blocks and avoid the AttributeError that occurred previously.