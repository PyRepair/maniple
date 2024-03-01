### Bug Explanation
The bug in the `equals` function arises from the comparison of `Block` objects in `self_blocks` and `other_blocks`. The `canonicalize` function is used to sort the blocks based on their dtype name and `mgr_locs`. However, the bug surfaces because the dtype object is not hashable, causing an error when trying to `sort` the blocks based on it.

### Bug Fix Strategy
To fix the bug, we need to modify the `canonicalize` function to not rely on the `dtype` object directly. Instead, we can convert the `dtype.name` to a hashable type. By converting the dtype name to a hashable form, we can ensure that the blocks can be properly sorted based on the desired criteria.

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
        return (str(block.dtype), block.mgr_locs.as_array().tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

In the corrected version, we convert `block.dtype` to a string before including it in the tuple within the `canonicalize` function. This ensures that the dtype names can be compared and sorted correctly, resolving the bug in the function.