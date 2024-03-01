### Bug Explanation
The bug in the `equals` function arises from the sorting of `self_blocks` and `other_blocks` based on the `canonicalize` function. The `canonicalize` function attempts to create a unique key for each block based on the block's `dtype.name` and `mgr_locs`. However, `block.dtype.name` is a dtype object, which cannot be directly converted to a `str`. This results in a 'TypeError' when trying to sort the blocks.

### Bug Fix
To fix this bug, we need to modify the `canonicalize` function to extract the name of the dtype as a string. Additionally, as the `mgr_locs` attribute seems to be a calculated attribute within the `Block` class, make sure it returns a comparable value for the blocks.

### Corrected Version
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
        return (str(block.dtype), list(block.mgr_locs))

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

In the corrected version, I modified the `canonicalize` function to extract the dtype name as a string and converted `block.mgr_locs` to a list for comparison. This should address the 'TypeError' issue and correctly compare the blocks in the `equals` function.