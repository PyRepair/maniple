### Bug Explanation:
The bug in the `equals` function is due to the comparison of blocks in a non-deterministic order. The function sorts the blocks in `self_blocks` and `other_blocks` based on a custom key function `canonicalize`, which is implemented with `sorted`. However, the `BlockPlacement` object within the `block` does not have a reliable comparison implementation, leading to blocks being ordered differently between `self` and `other`.

### Bug Fix Strategy:
To fix the bug, the sorting operation needs to consider both the `dtype.name` and the actual block data for comparison. If the comparison is based on the block's data itself rather than its location, the order of blocks in `self` and `other` should be consistent.

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

    # canonicalize block order based on dtype name and block data
    def canonicalize(block):
        return (block.dtype.name, block.to_numpy().tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By using `block.to_numpy().tolist()` in the `canonicalize` function, we ensure that the blocks are compared based on their actual data rather than their locations. This change should address the inconsistent block ordering issue and make the comparison deterministic, passing the failing test and resolving the GitHub issue.