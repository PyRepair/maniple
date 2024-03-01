### Bug Explanation
The bug occurs because the `equals` function is incorrectly comparing the data blocks of two BlockManagers. The comparison is based on the order of the blocks sorted by their datatype and manager locations. However, the block comparison logic is flawed, leading to incorrect results.

### Bug Fix Strategy
To fix the bug in the `equals` function, we need to ensure that the comparison of the data blocks between two BlockManagers is done correctly. This involves comparing the shape, data type, data values, and manager locations of the blocks between the two BlockManagers.

### Corrected Version of the `equals` function
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
    
    for block, oblock in zip(self.blocks, other.blocks):
        if not block.equals(oblock):
            return False
    
    return True
```

By comparing each block of the two BlockManagers correctly, based on the datatype, manager locations, and content, we ensure that the `equals` function returns the correct result.