The issue in the provided `equals` function is due to the use of `sorted` function on blocks, which may not guarantee the correct canonicalization order for blocks. To resolve this issue, we can sort the blocks based on the block metadata instead of the block itself, ensuring a consistent order for comparison.

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

    # canonicalize block order
    def get_block_key(block):
        return (str(block.dtype), block.mgr_locs.as_array.tobytes())

    self_blocks = sorted(self.blocks, key=get_block_key)
    other_blocks = sorted(other.blocks, key=get_block_key)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This corrected version uses a custom key function `get_block_key` to sort the blocks based on dtype and `mgr_locs`, ensuring a consistent order for comparison.

With this correction, the function will now correctly compare the blocks based on expected metadata and return the appropriate result.

This fix addresses the reported bug in the GitHub issue where the function was returning `True` incorrectly for different block locations.