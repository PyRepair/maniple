The bug in the `equals` function arises from comparing blocks in a different order due to unconsolidated blocks like Categorical. To fix this, we need to sort the blocks based on a canonicalization function that considers both dtype name and mgr_locs (which represent block locations). 

Below is the corrected version of the `equals` function:

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
    
    # canonicalize block order by sorting blocks
    def canonicalize(block):
        return (block.get_values().dtype.name, block.mgr_locs)
    
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This corrected version addresses the issue reported on GitHub and should now return the expected output for the failing test case.