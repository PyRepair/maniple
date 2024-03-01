The issue in the `equals` function seems to stem from comparing blocks with identical content but different locations. The `canonicalize` function is used to sort the blocks based on their type name and locations, attempting to address this issue. The `canonicalize` function is used to create a tuple of the block's type name and locations, which is then used for sorting.

To fix the bug, we need to ensure that the sorting mechanism used by the `canonicalize` function considers the block's content as well.

Here's the corrected version of the `equals` function:

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

    # canonicalize block order, considering content and locations
    def canonicalize(block):
        return (block.values, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By including the `block.values` in the `canonicalize` function, we ensure that blocks with identical content but different locations are distinguished correctly. This modification should resolve the issue reported on GitHub and allow the failing test to pass.