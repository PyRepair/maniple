### Bug Explanation:
The bug in the `equals` function lies in the order in which the blocks are sorted and compared between `self` and `other`. The bug is causing the comparison to return incorrectly because the sorting of the blocks is not consistent due to unconsolidated blocks like Categorical, which results in different orders for seemingly equal blocks.

### Bug Fix Strategy:
To address the bug, we need to ensure a consistent sorting mechanism for the blocks. One way to achieve this is to sort the blocks based on both the dtype name and the mgr_locs (block placement), ensuring a stable sorting order that can identify the blocks accurately.

### Corrected Version of the Function:
```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes) or not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False

    self._consolidate_inplace()
    other._consolidate_inplace()

    if len(self.blocks) != len(other.blocks):
        return False

    def canonicalize(block):
        return (block.dtype.name, tuple(block.mgr_locs))

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)

    return all(block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks))
```

By sorting the blocks based on a tuple of dtype name and block placement, we ensure a consistent comparison order, thus fixing the bug and enabling the `equals` function to return the correct result.