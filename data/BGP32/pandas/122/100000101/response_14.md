The bug in the provided function arises from the way the `canonicalize` function is sorting the `self_blocks` and `other_blocks`. The `canonicalize` function is sorting the blocks based on the tuple `(block.dtype.name, block.mgr_locs.as_array.tolist())`, but the `mgr_locs` attribute does not exist in the `IntBlock` or `ObjectBlock` classes.

To fix the bug, we need to modify the `canonicalize` function to only include `block.dtype.name` in the tuple for sorting.

Here is the corrected version of the function:

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

    def canonicalize(block):
        return block.dtype.name

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

With this correction, the function will now correctly compare the blocks based on their data type names only for sorting, addressing the bug in the original implementation.