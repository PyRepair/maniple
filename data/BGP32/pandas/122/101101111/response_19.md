### Bug Explanation:
The bug in the `equals` function arises due to the sorting logic based on block properties. When comparing two dataframes, if the blocks within the dataframes are in the same order but have different locations, the function incorrectly returns `True`. This is due to the sorting logic prioritizing type and location, but not considering the equality check on the blocks themselves, leading to identical blocks with different locations being considered equal.

### Bug Fix Strategy:
To fix this bug, the sorting logic needs to be modified to also consider the equality of the blocks themselves, not just their dtype and location. This way, even if the blocks have different locations but are identical, they will be correctly identified as unequal.

### Corrected Function:
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
    
    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array.tolist(), block.values)
    
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

### Expected Outcome:
With the corrected `equals` function, the failing tests, such as the one provided, should now correctly identify dataframes where identical blocks have different locations as unequal. This fix aligns with the expected behavior and resolves the reported GitHub issue.