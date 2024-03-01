### Bug Explanation:
The bug in the `equals` method of `BlockManager` is caused by not properly handling the case when blocks have identical data but different locations. The method currently compares blocks based on their data types and memory locations, which can lead to incorrectly returning `True` for blocks with the same data but different locations. This issue is identified by the failing test `test_dataframe_not_equal`, where two DataFrames with the same data but different column orders are incorrectly identified as equal.

### Bug Fix Strategy:
To fix this bug, we need to update the `equals` method of `BlockManager` to compare blocks based on the actual data they contain, rather than their memory locations. This can be achieved by comparing the values within blocks instead of relying on their order or memory addresses.

### Corrected Version:
Here is the corrected version of the `equals` method in `BlockManager`:

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

    self_blocks = sorted(self.blocks, key=lambda x: (x._get_values().tostring(), x.dtype))
    other_blocks = sorted(other.blocks, key=lambda x: (x._get_values().tostring(), x.dtype))

    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This corrected version sorts the blocks based on the actual values they hold before comparing them in the `equals` method, ensuring that blocks with identical data but different locations are correctly identified as not equal.