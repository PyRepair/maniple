The bug in the `equals` function is due to comparing the `mgr_locs` attribute of the blocks which are not comparable directly. To fix this bug, we need to modify the `equals` function to compare the `values` attribute of the blocks instead of `mgr_locs`.

Here's the corrected version of the `equals` function:
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

    self_blocks = sorted(self.blocks, key=lambda block: block.values)
    other_blocks = sorted(other.blocks, key=lambda block: block.values)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

This modification ensures that the blocks are sorted based on their `values` attribute, making them comparable for equality checks.

By implementing this change, the function should now correctly compare the blocks and return the expected output indicated in the GitHub issue.