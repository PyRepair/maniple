## Analysis:
The buggy function `equals` compares two `BlockManager` objects for equality by checking the equality of their axes and blocks. However, the function fails to correctly compare the blocks due to a sorting issue in the `canonicalize` function.

The test `test_dataframe_not_equal` creates two data frames with swapped values and expects `df1.equals(df2)` to be `False`. The issue reported on GitHub indicates that the function wrongly returns `True` in such cases.

## Identified issue:
The bug arises from the sorting order in the `canonicalize` function, which considers only the dtype name and block manager locations (mgr_locs). Because of this, unconsolidated blocks with different data are not handled correctly.

## Solution:
To fix the bug, we need to modify the `canonicalize` function to consider both dtype name and the actual data in the block while sorting the blocks.

## Corrected Code:
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
        return (block.dtype.name, block.values)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)

    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

With this correction, the function will now consider the actual values in the block while sorting, ensuring that unconsolidated blocks with different data are handled correctly. This correction should resolve the issue reported on GitHub and make the `equals` function behave as expected.