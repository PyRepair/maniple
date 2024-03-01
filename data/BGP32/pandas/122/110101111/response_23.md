Based on the issue description and the failing test provided, the bug in the `equals` function of the `BlockManager` class is that it is wrongly returning `True` when comparing DataFrames with identical blocks but different locations. The issue seems to be related to how the blocks are sorted and compared.

### Analyzing the Bug:
- The buggy function, `equals`, compares the axes, consolidates the blocks in place, sorts the blocks, and then checks if each block equals the corresponding block in the other `BlockManager`. The issue arises when there are identical blocks in different locations.
- The failing test `test_dataframe_not_equal` aims to compare DataFrames `df1` and `df2`, both having columns 'a' and 'b' but different data in those columns.

### Error Location:
- The root cause of the bug seems to be with the sorting mechanism used for blocks comparison and the handling of block locations.

### Bug Fix Strategy:
- To fix the bug, ensure that the blocks are compared correctly regardless of their exact location but with the actual data within them.

### Corrected Version of the `equals` Function:
```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes):
        return False
    if not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False

    self_blocks = [blk.values for blk in self.blocks]
    other_blocks = [blk.values for blk in other.blocks]

    return all(
        pd.testing.assert_frame_equal(s_blk, o_blk) is None
        for s_blk, o_blk in zip(self_blocks, other_blocks)
    )
```

By modifying the `equals` function to compare the block values directly and utilize `pd.testing.assert_frame_equal` for DataFrame comparison, the corrected version should now accurately determine equality even when blocks are in different locations. This fix aligns with the expected outcome of the failing test and should address the issue reported on GitHub.