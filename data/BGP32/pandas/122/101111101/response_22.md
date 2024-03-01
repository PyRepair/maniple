### Bug Explanation
The bug in the `equals` function stems from the sorting logic based on block properties. The function uses a `canonicalize` function to generate a tuple for each block, combining the block's dtype name and its `mgr_locs` attribute. However, the comparison of these tuples doesn't consider the specific values in the blocks.

In the failing test case, `df1` and `df2` both have columns 'a' and 'b' but with different data types and values. The buggy `equals` function incorrectly considers the data types and block indices but fails to account for the actual values within each block, leading to incorrect equality evaluation.

### Fix Strategy
To fix the bug, the `canonicalize` function should incorporate the data values in addition to dtype name and block indices. By including the actual values in the comparison, we ensure that two blocks are considered equal only if their data values match.

### Corrected Version of the Function
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

    # canonicalize block order considering dtype, values, and mgr_locs
    def canonicalize(block):
        return (block.values, block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.values.equals(oblock.values) and block.dtype.name == oblock.dtype.name and block.mgr_locs.equals(oblock.mgr_locs)
        for block, oblock in zip(self_blocks, other_blocks)
    )
```

By including the actual data values in the comparison and ensuring the dtype and mgr_locs match, the corrected function should now correctly evaluate the equality of blocks based on all relevant attributes.