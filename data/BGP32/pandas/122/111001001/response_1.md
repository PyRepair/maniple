#### Bug Explanation
The bug in the `equals` function lies in how the blocks are compared for equality. The function sorts the blocks based on a canonical form that combines the dtype name and the manager locations, with the assumption that this ordering will correctly match corresponding blocks in `self` and `other`. However, the comparison of blocks using `equals(oblock)` does not consider the manager locations, leading to incorrect results if the blocks are not in the same order due to unconsolidated blocks.

#### Bug Location
The bug is in the comparison block where `block.equals(oblock)` is being used, assuming that the blocks are correctly ordered based on the canonical form.

#### Strategy for Fix
To fix the bug, we can modify the comparison logic to consider the equality of blocks based on both the dtype name and the manager locations. This adjustment ensures that blocks are correctly matched even if their order may vary due to unconsolidated blocks.

#### Corrected Version
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
        return (block.dtype.name, block.mgr_locs.as_array().tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)

    return all(block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks))
```