### Bug Explanation:
The bug in the `equals` function arises from sorting the `self_blocks` and `other_blocks` lists based on the `canonicalize` function, which is defined to include the block's data type name and `mgr_locs`. However, the comparison of `mgr_locs` using `as_array.tolist()` might lead to inconsistent results.

### Bug Fix Strategy:
To fix the bug, we should ensure that the block comparison considers the data within the blocks rather than their locations.

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

    self_blocks = self.blocks
    other_blocks = other.blocks

    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By removing the sorting based on `canonicalize` and directly comparing the blocks, we avoid the inconsistency issue related to the block locations. This corrected version should address the problem reported in the GitHub issue.