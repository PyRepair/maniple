The problem has to do with the block comparison, specifically, the supposed block is getting identified as an equal block because the dtype and mgr_locs are the same, when it really shouldn't be. By adding a block shape comparison into your canonicalize() function, you'll eliminate this false positive.

The corrected code will look like this:

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
    # name, the shape of the block and then mgr_locs because there might 
    # be unconsolidated blocks (say, Categorical) which can only 
    # be distinguished by the iteration order
    def canonicalize(block):
        return (block.dtype.name, block.shape, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By adding the `block.shape` attribute to the `canonicalize()` comparison function, you'll ensure that blocks of different shapes are not mistakenly identified as identical. Remember to update your test script to reflect these changes.