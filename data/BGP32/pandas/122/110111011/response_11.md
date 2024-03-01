### Explanation:
The `equals()` function in the `BlockManager` class is comparing two instances of `BlockManager` objects to determine if they are equal. The function first checks if the axes of both objects are of the same length and if all corresponding axes are equal. Then it consolidates the blocks within each object and compares the blocks based on their data.

The bug arises from the way blocks are being sorted and compared. The function `canonicalize` is used to sort the blocks by their type name and locations. However, the `as_array.tolist()` call in `canonicalize` causes a list of lists to be returned, leading to incorrect comparison results.

The failing test, `test_dataframe_not_equal()`, demonstrates this issue by creating two dataframes with columns having different types and values. When comparing these dataframes using the `equals()` function, it wrongly returns True because of the incorrect block comparison logic.

### Fix Strategy:
To fix the bug, the `canonicalize` function should return a tuple containing the type name and locations without converting the locations to a list. This way, the blocks can be properly sorted and compared based on their data type and locations.

### Corrected Version:
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
        return (block.dtype.name, tuple(block.mgr_locs.as_array))

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By making this change, the blocks will be correctly sorted and compared without converting the locations to a list, resolving the incorrect True return issue in the failing test.