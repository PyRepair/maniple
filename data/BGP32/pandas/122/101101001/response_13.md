### Bug Explanation
The bug in the `equals` function is related to how the `self_blocks` and `other_blocks` are sorted and compared. The bug stems from the `canonicalize` function that is used to define the sorting key. The issue arises from calling `mgr_locs.as_array.tolist()` which doesn't return the representation needed for proper sorting.

### Bug Fix Strategy
To fix the bug, we need to change the way the `canonicalize` function creates the sorting key for the blocks. Instead of using `mgr_locs.as_array.tolist()`, we should use a more appropriate representation of the block for sorting.

### Corrected Version of the equals function
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

    # canonicalize block order based on dtype names
    def canonicalize(block):
        return block.dtype.name

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By modifying the `canonicalize` function to use `block.dtype.name` for sorting, we ensure a consistent and appropriate representation for comparing the blocks. This should resolve the bug and make the test function `test_dataframe_not_equal` pass.