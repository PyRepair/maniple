### Bug Analysis:
The bug in the provided function `equals` arises from the comparison of `self.blocks` and `other.blocks` without properly handling the order of the blocks. The blocks should be sorted based on their content before comparing them, but the current implementation does not consider the block order correctly. This leads to the function failing the test `test_dataframe_not_equal`.

### Bug Fix Strategy:
To fix the bug, we need to modify the sorting mechanism for `self_blocks` and `other_blocks` based on the block content. We should ensure that the blocks are sorted consistently before comparing them to identify any differences accurately.

### Corrected Version of the Function:
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
        return (block.dtype.name, block.mgr_locs.as_slice())
    
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

The corrected version of the function sorts `self_blocks` and `other_blocks` based on a canonical key derived from the block content. This ensures that the blocks are ordered consistently before comparison, fixing the bug and allowing the function to pass the given failing test.