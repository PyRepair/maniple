The bug in the `equals()` function is caused by the inconsistent comparison of dataframes. The function currently sorts the blocks by their dtype name and `mgr_locs`, but it should actually compare the sorted blocks based on their values to determine equality.

To fix the bug, we need to redefine the `canonicalize()` function to include the block values as well. Then, we can sort the blocks based on this new key function and compare the values of each block to check for equality.

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

    def canonicalize(block):
        return (block.values, block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        np.array_equal(block.values, oblock.values) for block, oblock in zip(self_blocks, other_blocks)
    )
```

With this corrected version of the `equals()` function, the test case `test_dataframe_not_equal()` should pass successfully.