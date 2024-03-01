### Bug Explanation:
The bug in the `equals` function is likely due to the sorting logic of `self_blocks` and `other_blocks`. The blocks are sorted based on a tuple combining the type name and `mgr_locs`, which can lead to incorrect outcomes if the sorting is not consistent.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the sorting mechanism for `self_blocks` and `other_blocks` is consistent and correct.

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

    # sorting the blocks based on a consistent key
    def sort_key(block):
        return (type(block).__name__, block.mgr_locs.as_slice().start)

    self_blocks = sorted(self.blocks, key=sort_key)
    other_blocks = sorted(other.blocks, key=sort_key)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

In the corrected version, `sort_key` function is used to establish a consistent sorting order for the blocks based on the block type name and starting position of `mgr_locs`. This should ensure proper equality checks between blocks in the `equals` function.