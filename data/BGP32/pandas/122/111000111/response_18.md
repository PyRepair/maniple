### Bug Explanation:
The bug in the `equals` function arises from the sorting logic of `self_blocks` and `other_blocks`. The blocks are sorted based on a tuple combining the type name and `mgr_locs`. If the blocks have the same type but different location arrays, they may end up being considered equal even though they are not.

### Bug Fix Strategy:
To fix the bug, we need to compare the blocks based on the type name and the actual values in the blocks, rather than relying on the location arrays.

### Corrected Version of the Function:
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

    # canonicalize block order based on type name
    def canonicalize(block):
        return block.dtype.name

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    if len(self_blocks) != len(other_blocks):
        return False
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By sorting the blocks based on the type name and comparing them directly, we ensure that the blocks are considered equal only if their types and values match. This corrected version should address the issue reported in the GitHub bug.