The bug in the `equals` function is caused by the problem with comparing `Block` objects and their locations without properly considering the consolidation of blocks. The function is sorting blocks based on the tuple of the block's data type name and locations, but it does not handle blocks that have not been consolidated. This leads to incorrect comparison results.

To fix the bug, before comparing the blocks, both `self` and `other` BlockManagers should be consolidated to ensure that the blocks are in a consistent state for comparison. Consolidation ensures that the blocks are combined and sorted correctly. Once the blocks are consolidated, the function can proceed with sorting and comparing the blocks. 

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

With this correction, the `equals` function should now properly handle the comparison of DataFrame blocks, considering their consolidation state and order. This fix should address the issue reported on GitHub and ensure that the function passes the failing test case.