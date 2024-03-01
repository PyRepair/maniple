### Bug Explanation
The bug in the `equals` function arises from the comparison of blocks within the `self_blocks` and `other_blocks` lists. The comparison is being performed based on the `equals` method of the blocks, which is currently incorrect. The comparison needs to be based on the actual values inside the blocks rather than the objects themselves.

### Bug Fix Strategy
1. Update the `canonicalize` function to return a tuple of the block values along with the block type.
2. Update the comparison step to compare the block values directly rather than using the `equals` method.

### Corrected Version of the `equals` Function
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
        return (block.values, block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)

    return all(
        np.array_equal(block.values, oblock.values) and
        block.dtype.name == oblock.dtype.name for block, oblock in zip(self_blocks, other_blocks)
    )
```

With this corrected version, the `equals` function will compare blocks based on their actual values, ensuring that the comparison is accurate. This should resolve the failing test case.