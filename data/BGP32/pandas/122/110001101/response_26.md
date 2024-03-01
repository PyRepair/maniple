The bug in the `equals` function lies in the comparison of blocks where the `canonicalize` function is used to sort the blocks based on their type and locations. The issue arises from accessing `dtype.name` directly on the block, which is not the correct attribute to retrieve the data type in this context.

To fix this bug, we should modify the `canonicalize` function to properly extract the data type of the block. We can achieve this by accessing the `dtype` attribute directly from the block.

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

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        return (str(block.dtype), block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By making this adjustment to correctly extract the data type of the block, the `equals` function should now work as expected and pass the failing test cases.