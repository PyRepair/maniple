### Bug Explanation:
The bug in the `equals()` function arises from the comparison of blocks in different orders. In the current implementation, the function sorts the blocks based on their type name and manager locations, assuming that unconsolidated blocks (like Categorical blocks) can only be distinguished by their iteration order. However, this can lead to incorrectly identifying blocks as equal when they are not due to a difference in order.

### Fix Strategy:
To fix the bug, we need to modify the comparison logic to ensure that the blocks are compared based on their values rather than their sorting order, which may be incorrect due to unconsolidated blocks. By directly comparing the values of the blocks, we can accurately determine if two DataFrames are equal.

### Corrected Version of the Function:
Here is the corrected version of the `equals()` function:

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

This corrected version directly compares the blocks present in `self` and `other` based on their values rather than their order.

By using this revised logic, the issue reported on GitHub where `df1.equals(df2)` wrongly returns `True` in the case of identical blocks with different locations should be resolved, and the corrected function should now return `False` as expected.