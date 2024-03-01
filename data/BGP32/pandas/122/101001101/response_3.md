### Bug Explanation:
The bug in the `equals` function arises from the comparison of blocks between `self` and `other`. The comparison of blocks is done based on their dtype name and manager locations. However, the comparison fails when the dtype names and manager locations are not properly handled or sorted.

### Bug Fix Strategy:
1. Ensure that the dtype name and manager locations are correctly retrieved and sorted for comparison.
2. Verify that the block comparison logic is accurate and handles all cases properly.

### Corrected Version:
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
        return (str(block.dtype), block.mgr_locs.as_array().tolist())
    
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

The corrected version ensures proper sorting and comparison of blocks based on dtype name and manager locations, fixing the bug in the `equals` function.