### Bug Explanation
The bug in the `equals` function arises from the way the blocks are compared between two `BlockManager` instances. The comparison involves sorting the blocks based on their data type name and location, which can lead to incorrect results due to unconsolidated blocks not being compared correctly.

### Bug Fix Strategy
To fix the bug in the `equals` function:
- We need to ensure that the comparison of blocks takes into account the actual data values in the blocks rather than just their data type and location.

### Corrected Version
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

    return all(
        block.equals(oblock) for block, oblock in zip(self.blocks, other.blocks)
    )
```

With this corrected version, the comparison now directly compares the blocks' content rather than relying on sorting based on data type names and locations. This change should fix the bug and allow the failing test `test_dataframe_not_equal` to pass.