### Bug Explanation:
The bug in the provided function arises from the usage of the `canonicalize` function to sort the `self_blocks` and `other_blocks`. The `canonicalize` function in the buggy code attempts to retrieve the `dtype.name` and `mgr_locs` attributes of a block to create a sorting key for the `sorted` function. However, in the buggy code, `block` is iterating over the blocks directly, which does not contain `dtype` and `mgr_locs` directly. Instead, we have to access these attributes from the `values` of the block.

### Bug Fix Strategy:
To fix the bug in the function, we need to modify the `canonicalize` function to correctly extract the `dtype.name` and `mgr_locs` attributes from the block values while iterating over the blocks.

### Corrected Version of the function:
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
        return (block.values.dtype.name, block.values.mgr_locs.as_array().tolist())
    
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By modifying the `canonicalize` function to extract attributes from `block.values`, we ensure that the comparison is done correctly based on the expected attributes of the blocks.