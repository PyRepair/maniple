## Bug Explanation

The bug in the `equals` function arises from the use of the `canonicalize` function to sort the blocks. The `canonicalize` function attempts to convert `block.mgr_locs.as_array.tolist()` to a list, but the correct call should be `block.mgr_locs.as_array().tolist()`, since `as_array` is a method, not a property.

## Fix Strategy

To fix this bug, we need to modify the `canonicalize` function to correctly call `as_array()` instead of `as_array`. This will ensure that `block.mgr_locs.as_array().tolist()` is used for both `self_blocks` and `other_blocks`.

## Corrected Version

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

By making this change, the bug related to the `equals` function's incorrect behavior will be resolved, which aligns with the expected values and types during the test execution.