### Bug Explanation:
The bug occurs in the `equals` method of the `BlockManager` class when comparing two instances of `BlockManager` objects. The bug arises due to the incorrect comparison of blocks within the `BlockManager` objects.

In the failing test function `test_dataframe_not_equal`, two DataFrames `df1` and `df2` are created with swapped column types. When calling the `equals` method on these DataFrames, the function incorrectly returns `True` instead of `False`. This happens because the function does not correctly compare the blocks within the `BlockManager` objects, leading to the wrong equality result.

### Bug Fix Strategy:
The bug can be fixed by modifying the comparison logic for blocks within the `BlockManager` objects. We need to ensure that the blocks are correctly compared based on their dtype and locations.

### Corrected Function:

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
        return (block[0].dtype.name, block[1].mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks.items(), key=canonicalize)
    other_blocks = sorted(other.blocks.items(), key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

### Changes Made:
1. Modified the `canonicalize` function to correctly extract the dtype and mgr_locs from the block tuples.
2. Sorted the `self.blocks` and `other.blocks` dictionaries by the `canonicalize` key.
3. Updated the comparison inside the `all` function to compare the blocks correctly.

By making these changes, the corrected function should now pass the failing test and provide the expected output.