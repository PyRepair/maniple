The bug in the provided function lies in the sorting logic of `self_blocks` and `other_blocks`. The function is using a tuple of `dtype.name` and `mgr_locs.as_array.tolist()` to compare and sort the blocks. However, `mgr_locs.as_array.tolist()` is not a valid attribute of `mgr_locs`, resulting in an AttributeError. 

To fix this bug, we should update the `canonicalize` function to consider only the `dtype.name` for sorting and comparison, as the `mgr_locs` attribute is not applicable in this context.

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

With this fix, the function will correctly compare and sort the blocks based on the `dtype.name` attribute only, resolving the AttributeError and ensuring the function behaves as expected.