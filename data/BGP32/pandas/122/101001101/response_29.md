### Cause of the bug
The bug in the `equals` function arises from the sorting of `self_blocks` and `other_blocks`. The function uses a `canonicalize` function to generate a key for sorting based on `dtype.name` and `mgr_locs` of each block. However, the `mgr_locs` attribute is being accessed incorrectly as a method (`as_array.tolist()`) instead of just as an attribute. This leads to a runtime error and incorrect comparison of blocks.

### Strategy for fixing the bug
To fix the bug, we need to update the `canonicalize` function to correctly access the `mgr_locs` attribute of the blocks. Since `mgr_locs` is an attribute, we should directly access it without calling it as a method. This will ensure that the sorting logic works correctly.

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

    # Correct the canonicalize function to access mgr_locs attribute correctly
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

By updating the `canonicalize` function to correctly access `mgr_locs` and removing the unnecessary method calls, the function should now work correctly and pass the failing tests.