### Bug Explanation
The bug in the `equals` function arises from the sorting operation on the `self_blocks` and `other_blocks` lists. The sorting is done based on a tuple that combines the block's dtype name and its `mgr_locs` attribute. However, the `mgr_locs` attribute needs to be converted to a list before being sorted. The buggy code attempts to call `as_array` directly on the `mgr_locs`, resulting in the error.

### Bug Fix Strategy
To fix the bug, we need to update the `canonicalize` function to correctly extract a list from the `mgr_locs` attribute by calling `as_array` and then converting it to a list using `tolist()`.

### Corrected Version of the Function

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

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array().tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

By converting `mgr_locs` to a list correctly before sorting, the function should work as expected and pass the failing test.