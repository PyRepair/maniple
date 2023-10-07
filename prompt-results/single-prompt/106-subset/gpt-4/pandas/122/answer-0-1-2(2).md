From the error, it is clear that the `DataFrame.equals()` method is returning `True` even when the two dataframes are not equal.

The `equals()` function compares the types and values within the dataframes, but it fails to address the situation when the two dataframes have identical blocks but in different locations. 

To fix this issue, the reference to `mgr_locs` should be changed from `mgr_locs.as_array.tolist()` to `tuple(mgr_locs.as_array)`. This change will allow the `mgr_locs` (Manager Locations) to be compared correctly, thereby addressing the bug.

Here is the corrected function:

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

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        # Changes made in the following line of code
        return (block.dtype.name, tuple(block.mgr_locs.as_array))

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

With this corrected function, the test `test_dataframe_not_equal()` should return `False` as expected, because `df1` and `df2` are not equal.