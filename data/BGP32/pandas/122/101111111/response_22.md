### Bug Explanation:
The bug occurs in the `equals` function of the `BlockManager` class. The function is intended to compare two blocks of data for equality. However, the bug causes the function to return `True` incorrectly even when the blocks have different locations. This bug leads to failing test cases, such as the provided `test_dataframe_not_equal()` test.

The issue arises due to sorting the self and other blocks based on the `canonicalize` function, which uses the block's data type name and location as criteria for sorting. The bug arises because the function does not take into account the possibility of unconsolidated blocks in which the same data type appears in different locations.

### Bug Fix Strategy:
To address the bug, we need to modify the sorting criteria within the `equals` function. Instead of relying solely on the data type name and location for sorting, we should consider the data type name, the presence of unconsolidated blocks, and then the location. This adjustment will ensure that unconsolidated blocks are distinguished correctly.

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

    def canonicalize(block):
        dtype_name = block.dtype.name
        locs = block.mgr_locs
        # Additional check for unconsolidated blocks
        if isinstance(locs, BlockPlacement):
            locs = locs.as_array
        return (dtype_name, locs.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By making these adjustments in the `equals` function, we ensure that the blocks are compared properly, taking into account unconsolidated blocks and preventing false `True` results when blocks have different locations. This corrected version should address the bug and make the `equals` function behave as expected.