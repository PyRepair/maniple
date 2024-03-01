### Bug Explanation:
The bug in the `equals` function is caused by the incorrect comparison and ordering of the `self_blocks` and `other_blocks`. The function attempts to sort the block data of `self` and `other` by `dtype` and `mgr_locs`, but the comparison logic is flawed.

In the failing test scenario provided:
- `df1` consists of integer values in column "a" and string values in column "b".
- `df2` consists of string values in column "a" and integer values in column "b".

The incorrect comparison logic in the `equals` function leads to a false positive comparison result, which is why the failing test `test_dataframe_not_equal` detects the issue.

### Fix Strategy:
To fix the bug in the `equals` function, we need to ensure that the comparison between blocks of `self` and `other` occurs by matching the columns correctly. The comparison logic should focus on comparing the actual data within the blocks rather than the order based on dtype and mgr_locs.

### Corrected Code:
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
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By comparing the actual block data in `self_blocks` and `other_blocks`, we avoid the issue of mismatching the columns and ensure that the function correctly identifies when two DataFrames are not equal.