### Bug Explanation
The bug in the `equals` function is caused by incorrect block comparison due to unsorted blocks. The function compares the blocks between two instances of `BlockManager`, but it does not ensure that the blocks are in the same order before comparing them. This leads to false negatives in the logic of the function, causing it to return `False` even when the dataframes should be considered equal.

### Bug Fix Strategy
To fix the bug, we need to ensure that the blocks in both `self` and `other` are sorted before comparing them. By sorting the blocks based on a canonicalization function that combines the block data type name and the manager locations, we can guarantee that the comparison is done correctly even for unconsolidated blocks.

### Corrected Version of the `equals` Function
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

    # canonicalize block order
    def canonicalize(block):
        return (block.ftype, block.mgr_locs)  # updated to compare ftype and mgr_locs

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)

    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By sorting the blocks based on the `ftype` and `mgr_locs` before the comparison, the corrected function appropriately handles the comparison of blocks and the overall equality check between two instances of `BlockManager`. This should resolve the failing test case provided.