### Bug Explanation
The bug in the `equals` function stems from the comparison of `self_blocks` and `other_blocks`. The blocks are not being handled correctly, leading to the assertion failure in the test `test_dataframe_not_equal`. The function compares blocks' equality based on their dtype name and memory locations, which is not correct for determining if two DataFrames are equal.

### Bug Fix Strategy
To fix the bug, we need to compare the data within the blocks instead of the dtype names and memory locations. We can achieve this by comparing the data values directly.

### Corrected Version of the Function
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

    self_blocks = self.blocks
    other_blocks = other.blocks

    return all(
        np.array_equal(block.values, oblock.values)
        for block, oblock in zip(self_blocks, other_blocks)
    )
```

In this corrected version, we compare the values of corresponding blocks directly by using `np.array_equal`. This ensures that the actual data within the blocks is compared for equality.

By implementing this fix, the `equals` function should now correctly compare DataFrames and pass the failing test.