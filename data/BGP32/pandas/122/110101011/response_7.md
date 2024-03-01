### Analysis:
1. The `equals` method in the `BlockManager` class is implemented to compare two instances of `BlockManager`. It checks the equality of axes and blocks between the two instances.
2. In the failing test `test_dataframe_not_equal`, two dataframes `df1` and `df2` are created with columns swapped. The `equals` method is called on these dataframes which should return `False`.
3. The bug in the current implementation arises due to the sorting of blocks based on a combination of dtype name and mgr_locs which might lead to considering blocks with different locations as equal, causing the function to return `True` incorrectly.
4. To fix the bug, we should modify the `canonicalize` function to generate a unique key for each block based on the dtype and values, ensuring that blocks with different locations are not incorrectly considered equal.
  
### Bug Fix:
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
        return (block.values, block.dtype.name)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By modifying the `canonicalize` function to use both the block values and dtype name, the comparison will be more robust and ensure that blocks with different locations are not incorrectly considered equal. This corrected version should pass the failing test and resolve the issue mentioned on GitHub.