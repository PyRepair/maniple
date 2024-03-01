### Explanation:
1. The function `equals` is designed to compare two `BlockManager` objects. It checks the equality of axes, consolidates the blocks, sorts them, and then compares the blocks for equality.
   
2. The error message indicates that the comparison `df1.equals(df2) is False` failed, resulting in `assert True is False`.

### Bug:
The bug is in the comparison of two DataFrames `df1` and `df2` where the values in columns 'a' and 'b' are interchanged between the two DataFrames. The bug is triggered because the function is expecting the values to be in the same order in both DataFrames.

### Strategy for fixing the bug:
To fix the bug, we can modify the function to compare the values of DataFrames without relying on the order of columns.

### The corrected version of the function:

```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes):
        return False
    if not all(set(ax1) == set(ax2) for ax1, ax2 in zip(self_axes, other_axes)):  # Compare set of axis values
        return False
    self._consolidate_inplace()
    other._consolidate_inplace()
    if set(self.blocks) != set(other.blocks):  # Compare set of blocks
        return False

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks which can only be distinguished by the iteration order
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By comparing the sets of axes and blocks in the corrected version of the function, we can ensure that the function works correctly even when the column order is different between DataFrames.