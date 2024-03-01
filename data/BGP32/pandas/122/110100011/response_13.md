## Analysis:
- The `equals` function in the `BlockManager` class is incorrectly comparing two instances by sorting blocks based on their datatype and manager locations. This can lead to instances with identical blocks but different locations being incorrectly marked as equal.
- The failing test case `test_dataframe_not_equal` creates two DataFrames with columns swapped and expects them to be unequal. However, the `equals` function currently returns `True` in such cases due to the bug.

## Error Locations:
- The error lies in the `canonicalize` function used for sorting the blocks based on datatype and manager locations.
- As a result, if two DataFrames have the same blocks but in different locations, they might be incorrectly marked as equal.

## Bug Cause:
- The bug originates from the way the `equals` function compares blocks between `BlockManager` instances.
- The sorting based on data type and manager locations does not guarantee correct comparison of blocks, leading to incorrect equality checks.

## Fix Strategy:
- Instead of comparing blocks directly, we should focus on comparing the data inside the blocks.
- Update the `canonicalize` function to compare the actual block data itself rather than sorting based on metadata like datatype and locations.

## Corrected Version:
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

    self_blocks = self._data.get_values()
    other_blocks = other._data.get_values()
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This corrected version compares the actual block values inside the `BlockManager` instances rather than metadata like data type and manager locations. This will ensure correct comparison of DataFrames and fix the bug reported in the GitHub issue.