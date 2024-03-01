### Explanation:
The bug occurs in the `equals` function of the `BlockManager` class where it wrongly returns True even when the two DataFrames have identical blocks with different locations. This bug causes the failing test `test_dataframe_not_equal` to assert `True is False`, revealing the incorrect behavior of the `equals` function.

The bug is due to the `_consolidate_inplace` method not being called before comparing the blocks, leading to the blocks not being consolidated making the equality check prone to incorrect results.

### Fixing Strategy:
To fix the bug, the `_consolidate_inplace` method needs to be invoked for both `self` and `other` instances of the `BlockManager` class before comparing the blocks. This will ensure that the blocks are properly consolidated before performing the equality check.

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

    # canonicalize block order, using a tuple combining the type
    # name and then mgr_locs because there might be unconsolidated
    # blocks (say, Categorical) which can only be distinguished by
    # the iteration order
    def canonicalize(block):
        return (block.dtype.name, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By incorporating the `_consolidate_inplace` calls before the block comparison, the corrected function ensures that the blocks are properly consolidated, resolving the issue and passing the failing test.