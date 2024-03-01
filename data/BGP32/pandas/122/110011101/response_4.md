### Bug Explanation
The bug in the `equals` function arises from the comparison of `block` and `oblock` within the `canonicalize` function. The `canonicalize` function is used to sort the blocks based on their type name and manager locations. However, the `block` object is identified incorrectly within the function, leading to a comparison error.

In the failing test case, the comparison is made between an `IntBlock` and an `ObjectBlock`, resulting in the `equals` method returning `True` instead of `False`. This discrepancy causes the test to fail.

### Fix Strategy
To fix the bug, we need to ensure that we are comparing blocks of the same type when sorting within the `canonicalize` function. We need to consider both the type name and the manager locations to correctly identify and sort the blocks.

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
        return (type(block).__name__, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

This corrected version ensures that we are comparing blocks of the same type, identified by the type name, before performing the equality check in the `equals` function.