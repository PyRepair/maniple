### Bug Explanation
The bug in the `equals` function arises from the comparison of the blocks in `self.blocks` and `other.blocks`. Due to unconsolidated blocks, the comparison is incorrect even when the blocks contain the same data but have different locations. This leads to the function incorrectly returning `True` instead of `False` as expected.

### Bug Fix Strategy
To fix this bug, we need to ensure that the comparison between blocks considers the content of the blocks accurately and handles cases where the blocks are identical but have different locations. We can achieve this by comparing the block data itself rather than the block references.

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

    def canonicalize(block):
        return (block.values)
  
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.values.equals(oblock.values) for block, oblock in zip(self_blocks, other_blocks)
    )
```

### Changes Made
- Updated the `canonicalize` function to compare block values instead of locations
- Sorted the blocks based on values for accurate comparison
- Compared block values using `equals` method

This corrected version should resolve the bug and improve the accuracy of the `equals` function when comparing blocks with different locations but identical content.