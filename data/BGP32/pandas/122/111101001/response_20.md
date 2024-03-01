### Bug Explanation
The bug in the `equals` function arises due to the comparison of blocks between `self` and `other` instances. The comparison fails when sorting the blocks because the `canonicalize` function compares the dtype name of the blocks and `mgr_locs` (which represents the block's location). In this scenario, the dtype name comparison is correct, but the comparison of `mgr_locs` as a list is incorrect due to a missing method call.

### Bug Fix Strategy
To fix the bug, we need to correct the comparison of `mgr_locs` by converting it to a list properly to be used as a key for sorting. This can be achieved by calling the `as_array` method on `mgr_locs` to get a list representation.

### Corrected Version

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
        return (block.dtype.name, block.mgr_locs.as_array().tolist())  # Fix: Convert mgr_locs to list

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By correcting the comparison key in the `canonicalize` function to include `mgr_locs` as a list properly, the comparison issue should be resolved, making the function behave correctly and pass the failing test.