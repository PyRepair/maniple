The bug in the `equals` function lies in the sorting of `self_blocks` and `other_blocks` using the `canonicalize` function. The `canonicalize` function returns a tuple of (`block.dtype.name`, `block.mgr_locs.as_array.tolist()`), but `block.dtype.name` will raise an AttributeError since `dtype` does not have the attribute `name`.

To fix this bug, we need to modify the `canonicalize` function to correctly handle the dtype attribute.

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

    # canonicalize block order, using a tuple combining the type name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by the iteration order
    def canonicalize(block):
        return (str(block._typ), block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

In this corrected version, we use `str(block._typ)` instead of `block.dtype.name` to get a string representation of the block type, which should resolve the AttributeError issue. This change ensures that the sorting process is done correctly based on the block type.

By making this adjustment, the `equals` function should now work as expected and pass the failing tests.