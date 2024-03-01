The issue in the `equals` function arises from the comparison of block order based on dtype and location, which leads to incorrect equality evaluation. The blocks for `df1` and `df2` have swapped locations, causing the function to return `True` incorrectly.

To fix the bug, we need to modify the `canonicalize` function to consider the manager locations for comparison. This ensures that blocks with the same data but different locations are not mistakenly considered equal.

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

    # Canonicalize block order based on dtype, and manager locations
    def canonicalize(block):
        return (block.mgr_locs.as_array.tolist(), block.dtype.name)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By modifying the `canonicalize` function to include manager locations in block comparison, the function should now correctly identify that `df1` and `df2` are not equal as intended. This change aligns with the expected behavior and resolves the bug reported on GitHub.