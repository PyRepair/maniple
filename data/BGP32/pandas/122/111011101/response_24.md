### Bug Explanation
The bug in the `equals` function arises from the comparison of `self.blocks` and `other.blocks`. The issue stems from not dealing with the contents of the blocks correctly. The blocks are sorted based on their types (`dtype.name`) and locations (`mgr_locs`), but the comparison should account for the actual data within the blocks.

### Bug Fixing Strategy
To fix the bug, we need to update the comparison logic in the `equals` function to properly compare the content of each block within `self` and `other`. We should compare the underlying data within each block while respecting the sorted order based on `dtype.name` and `mgr_locs`.

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

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.values.equals(oblock.values) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This corrected version compares the `.values` attribute of each block within `self_blocks` and `other_blocks` to ensure an accurate comparison of the block contents. This approach considers the actual data within each block while maintaining the ordering based on `dtype.name` and `mgr_locs`.