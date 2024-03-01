### Bug Explanation
The bug in the `equals` function arises from how the `canonicalize` function is sorting the blocks. It uses `block.dtype.name` as part of the sorting key, but `block.dtype` returns the data type of the block, not the name as expected. This leads to incorrect sorting and comparison of blocks, causing the function to return incorrect results.

### Bug Fix Strategy
To fix the bug, we need to modify the `canonicalize` function to use `block.dtype.name` correctly to obtain the data type name for sorting the blocks. This will ensure that the blocks are sorted based on their data type names, as intended.

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

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

By utilizing `block.dtype.name` within the `canonicalize` function, we ensure that the blocks are sorted correctly based on their data type names, resolving the bug.