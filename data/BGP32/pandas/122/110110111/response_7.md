### Bug Explanation:
- The `equals` function in the `BlockManager` class is intended to compare two instances of `BlockManager` objects for equality.
- The bug arises from the fact that the function is comparing blocks based on their dtype name and locations, which can lead to a false positive when the blocks are actually identical but have different locations.
- The failing test `test_dataframe_not_equal` creates two DataFrames with columns swapped and expects the `equals` function to return `False`, which it should according to the data being different.

### Bug Fix Strategy:
- To fix this bug, we need to modify the `canonicalize` function that determines the order in which blocks are compared. Instead of using dtype name and locations, we can compare the values directly to ensure accurate comparison.
- We should ensure that the function checks for the actual equality of block values rather than relying on metadata like dtype and locations.

### Corrected Version of the `equals` Function:
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
        block.values.equals(oblock.values) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By comparing the block values directly, this corrected version of the function should accurately determine the equality of `BlockManager` objects.