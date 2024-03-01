### Bug Explanation

The `equals` function is currently comparing blocks using a sorting approach that might result in inaccurate comparisons, especially when blocks have identical values but different locations. This can lead to the function wrongly returning `True`, causing the failing test to raise an assertion error.

- The failing test `test_dataframe_not_equal` creates two dataframes `df1` and `df2` with identical values in different locations for the columns. The test expects the `equals` function to return `False` since the dataframes are not equal.
- The error message indicates that the assertion `assert True is False` fails, suggesting that the `equals` function incorrectly returns `True`.
- The runtime values show that the function is incorrectly sorting blocks based on dtype name and location, which can lead to incorrect equality comparisons.

### Bug Fix Strategy

To fix the bug in the `equals` function, the comparison logic needs to be adjusted to take into account the actual content of the blocks rather than their sorting order based on dtype names and locations. By comparing the content of the blocks directly, the function can accurately determine equality between two dataframes.

### Corrected Function

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
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By directly comparing the blocks in the corrected function, the equality comparison between dataframes will be accurate, satisfying the expected output for the failing test.