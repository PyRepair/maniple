### Bug Explanation
The bug occurs in the `equals` function because when comparing the blocks, it does not correctly handle the case where the blocks are sorted based on their `dtype.name` and `mgr_locs`. The sorting is essential for comparison, especially when dealing with unconsolidated blocks like Categorical which can only be distinguished by the iteration order. In the failing test case, `df1` and `df2` have columns with different data types in different orders, resulting in a False assertion.

### Bug Fix Strategy
1. Ensure that the `canonicalize` function sorts the blocks based on both `dtype.name` and `mgr_locs` to maintain consistency.
2. Update the `equals` function to sort `self_blocks` and `other_blocks` before comparing them to ensure a consistent order for block comparison.

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

The corrected function now sorts `self_blocks` and `other_blocks` based on `dtype.name` and `mgr_locs` before comparing them, ensuring a consistent order for block comparison. The fix should address the bug in the original function.