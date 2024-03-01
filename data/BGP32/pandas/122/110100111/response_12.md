### Analysis:
1. The `equals` function in the `BlockManager` class is comparing two `BlockManager` instances by checking if their axes are equal and then comparing the blocks within them.
2. The bug seems to arise due to incorrect comparison logic in the function that does not handle the case where identical blocks have different locations.
3. The failing test is checking if two DataFrames with swapped column data are equal, which they are not since the column data is different.
4. To fix the bug, we need to refactor the comparison logic in the `equals` function to properly compare the blocks while considering their locations.
5. We need to ensure that the comparison of blocks is not solely based on order or location, taking into account the content of the blocks for equality.

### Proposed fix:
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

    # canonicalize block order, using a set of values within the block for equality comparison
    def canonicalize(block):
        return hash(tuple(block.values._data))

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By using the `values._data` attribute to create a hashable representation of block content for comparison, the function now properly compares the blocks' content for equality. This should resolve the issue reported on GitHub and make the function behave as expected.