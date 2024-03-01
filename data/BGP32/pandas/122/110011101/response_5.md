### Bug Explanation
The bug in the `equals` function arises due to the way blocks are sorted and compared in the `self_blocks` and `other_blocks` lists. The comparison is based on a tuple combining the type name and the locations of the blocks. However, the bug occurs because the `canonicalize` function, used to create this tuple, is not handling the `dtype.name` correctly. 

### Bug Location
The issue is in the `canonicalize` function where `block.dtype.name` is used to extract the type name. Since the `block` variable is of type `IntBlock`, the `dtype.name` returns `int64` instead of the expected string representation of the type. This incorrect representation affects the sorting and comparison logic of blocks.

### Fix Strategy
To fix the bug, we need to modify the `canonicalize` function to extract the type name properly. We should ensure that we get a string representation of the block's type that can be compared accurately. We can use `str(block.values.dtype)` to get the desired type name string.

### Corrected Version
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
        return (str(block.values.dtype), block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By using `str(block.values.dtype)` to extract the type name, we ensure that the comparison of blocks based on type works correctly, addressing the bug in the `equals` function.