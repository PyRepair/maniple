The issue is occurring because the `equals` method is not correctly handling the case when identical blocks have different locations. One possible fix for this issue is to replace the `mgr_locs` attribute with a more stable attribute that can be used to canonicalize the blocks.

Here's the modified code snippet with the fix:

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
        return (block.values.dtype.name, hash(block.values.tobytes()))

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

Note that in the `canonicalize` function, the `mgr_locs` attribute has been replaced with `hash(block.values.tobytes())`. This ensures that identical blocks with different locations will have the same canonicalization, allowing the equality check to work correctly.