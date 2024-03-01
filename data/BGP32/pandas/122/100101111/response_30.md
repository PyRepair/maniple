### Analysis:
1. The `equals` function compares two `BlockManager` objects by checking if their axes are equal, if the blocks are equal, and then compares the blocks using a canonicalization process.
2. The issue arises when processing blocks in `canonicalize` due to unconsolidated blocks, leading to incorrect identification of block equality.
3. The test function `test_dataframe_not_equal` expects `df1.equals(df2)` to return False, but due to the bug in the `equals` function, it may wrongly return True when blocks have different locations but are identical.
4. To fix the bug, we need to modify the comparison logic within the `equals` function to correctly handle unconsolidated blocks that may have different locations.

### Bug Fix Strategy:
1. Modify the `canonicalize` function to handle unconsolidated blocks properly by considering the block values instead of just the locations.
2. Update the block comparison in the main logic of the `equals` function to compare the block values directly for equality.
3. Ensure that the sorting and comparison process accounts for unconsolidated blocks and correctly identifies them as different if their values differ.

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

    def canonicalize(block):
        return block.values

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    if len(self_blocks) != len(other_blocks):
        return False

    return all(
        block.values.equals(oblock.values) for block, oblock in zip(self_blocks, other_blocks)
    )
```

The corrected version compares the block values directly in both the `canonicalize` function and the main comparison logic, ensuring correct identification of equality even for unconsolidated blocks that may have different locations. This modification should resolve the issue reported on GitHub and pass the failing test.