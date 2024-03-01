The bug in the `equals` function lies in the `canonicalize` function. The issue is with the line `block.dtype.name`, as the `dtype` attribute of a block doesn't have a `name` attribute which is causing the AttributeError.

To fix the bug, we need to access the type name using `str(block.dtype)` instead of `block.dtype.name`.

Here is the corrected version of the `equals` function:

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
        return (str(block.dtype), block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By using `str(block.dtype)` instead of `block.dtype.name`, we can avoid the AttributeError and ensure that the function works correctly.