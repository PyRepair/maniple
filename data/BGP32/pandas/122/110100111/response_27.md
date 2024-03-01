### Analysis:
1. The buggy function `equals(self, other)` compares two `BlockManager` objects for equality by comparing their axes and blocks.
2. The provided failing test `test_dataframe_not_equal()` creates two DataFrames with columns in a different order and expects `df1` and `df2` to not be equal.
3. The bug seems to be related to the comparison of blocks in the `BlockManager` objects, as different blocks with the same data cause `equals()` to return `True`.

### Bug:
The bug arises from the way blocks are compared in the `equals()` function. If blocks have identical data but different locations, they are incorrectly considered equal, causing the function to return `True` when it should return `False`.

### Strategy for Fixing the Bug:
To fix the bug, we should compare the blocks based on their data values rather than their locations. This can be achieved by sorting the blocks before comparison to ensure consistency in the order of blocks.

### Corrected Version of the `equals()` function:

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

    # sort blocks before comparison
    self_blocks = sorted(self.blocks, key=lambda block: block.values)
    other_blocks = sorted(other.blocks, key=lambda block: block.values)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By sorting the blocks based on their values before comparison, the corrected function ensures that identical blocks with different locations are correctly considered unequal. This fix should resolve the issue reported on GitHub and make the `equals()` function behave as expected.