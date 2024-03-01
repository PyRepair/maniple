### Bug Explanation
The bug in the `equals` function arises from the comparison of blocks in the `self_blocks` and `other_blocks` lists. The comparison is done based on the `equals` method of each block, which may not yield the correct result due to an issue in the block sorting mechanism. 

### Bug Location
The bug is located in the sorting process of `self_blocks` and `other_blocks`, where the `canonicalize` function constructs a key tuple using the block's dtype name and the mgr_locs values. If there are unconsolidated blocks, the sorting might not be consistent, leading to incorrect comparison results.

### Bug Fix Strategy
To fix the bug, we need to ensure that the blocks are consistently sorted for comparison. One approach is to sort based on dtype name first, and if they are equal, then sort based on mgr_locs values to maintain a stable order.

### Corrected Function
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
    
    # canonicalize block order, sorting blocks by dtype name and then mgr_locs
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array.tolist())
    
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By updating the sorting key function `canonicalize` to first sort by dtype name and then mgr_locs values, we ensure a stable and consistent order for block comparison, fixing the bug in the `equals` function.