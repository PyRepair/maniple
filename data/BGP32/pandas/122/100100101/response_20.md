### Bug Explanation
The bug in the `equals` function lies in the `canonicalize` function where `block.mgr_locs.as_array.tolist()` is used. The `mgr_locs` attribute of `block` should be accessed using dot notation, but in the buggy code, it is accessed as if it is a function. This results in an `AttributeError` when trying to call `as_array` on `mgr_locs`.

### Bug Fix Strategy
To fix the bug, we need to correctly access the `mgr_locs` attribute of the `block` object without calling it as a function.

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

    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

With this corrected version, the function should not throw an `AttributeError` when trying to access the `mgr_locs` attribute correctly.