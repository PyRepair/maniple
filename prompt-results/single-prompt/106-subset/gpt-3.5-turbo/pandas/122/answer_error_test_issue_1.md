The issue seems to be with the sorting of the `blocks` before comparing them in the `equals` method. Sorting them based on their dtype name and manager locations can cause incorrect comparison results when the blocks have the same data but different locations.

To fix this issue, we can modify the `canonicalize` function to only consider the dtype name for sorting. This way, blocks with the same data will be considered equal, regardless of their locations.

Here's the fixed code:

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

    # canonicalize block order, using the type name only
    def canonicalize(block):
        return block.dtype.name

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This change ensures that blocks with the same data will be correctly considered equal, regardless of their locations.

Please let me know if you have any questions or concerns.