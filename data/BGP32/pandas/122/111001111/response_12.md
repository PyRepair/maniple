### Bug Explanation
The bug occurs in the `equals` function of the `BlockManager` class. It incorrectly returns `True` even when the blocks have the same content but are in different locations. This happens due to the comparison of blocks in a non-canonicalized order, leading to a false positive result.

### Bug Fix Strategy
To fix the bug, we need to sort the blocks in a canonicalized order before comparing them. This ordering should consider the type name and the block locations to differentiate between unconsolidated blocks correctly.

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

    def canonicalize(block):
        return (str(block.dtype), block.mgr_locs.as_array())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

Now, by sorting the blocks based on the type and locations before comparing them, the `equals` function will deliver the correct result and address the issue reported on GitHub.