### Bug Explanation
The buggy function `equals` in the `BlockManager` class is failing the test `test_dataframe_not_equal` because it incorrectly sorts and compares the blocks in the `self` and `other` BlockManagers. The problem arises from the `canonicalize` function that creates a tuple with the type name and manager locations of each block for sorting. The bug occurs due to the comparison of blocks based on unconsolidated Manager locations. 

### Bug Fix Strategy
To fix the bug, we need to ensure that the comparison of blocks in the `equals` function is done correctly. Specifically, we should update the `canonicalize` function to handle unconsolidated blocks properly before sorting and comparing them. 

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

    # canonicalize block order, considering unconsolidated blocks
    def canonicalize(block):
        mgr_locs = block.mgr_locs if hasattr(block, 'mgr_locs') else None
        return (block.dtype.name, mgr_locs)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

The corrected version of the function now correctly handles the sorting and comparison of blocks, ensuring unconsolidated blocks are considered for comparison. This should now pass the failing test `test_dataframe_not_equal`.