### Issues and Bugs Identified:
1. The `equals` function is comparing the blocks without considering their order and location, leading to incorrect results.
2. The `canonicalize` function is not effectively handling distinguishing unconsolidated blocks.
3. The test case `test_dataframe_not_equal` is failing because the `equals` function is incorrectly returning True when it should be False due to the order and location of the blocks.

### Bug Cause:
The `equals` function is comparing blocks in an uncanonicalized order, leading to True being incorrectly returned even when the blocks have different order or locations. The `canonicalize` function should account for block order and location to accurately compare them.

### Fixing Strategy:
To fix the bug, we need to adjust the ordering of blocks in the `equals` function by using the `canonicalize` function effectively. By ensuring that we compare blocks in a canonicalized order that considers both type name and location, we can accurately determine equality.

### Corrected Version:
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

    # canonicalize block order, considering type name and mgr_locs
    def canonicalize(block):
        return (block.dtype.name, str(block.mgr_locs))

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

With this corrected version of the `equals` function, the comparison of blocks will be done in a properly canonicalized order that accounts for the block's type name and location. This change should address the bug and ensure accurate comparison results, passing the failing test and resolving the issue reported on GitHub.