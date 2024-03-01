### Bug Explanation:

The bug lies in the comparison logic in the `equals` function of the `BlockManager` class. The function compares the blocks directly without considering the order or locations of the blocks, leading to the wrong equality comparison.

### Bug Fix Strategy:

1. The bug can be fixed by modifying the comparison logic to consider not only the block content but also the order and locations of the blocks.
2. We need to sort the `self.blocks` and `other.blocks` based on a canonical key that includes the block type name and locations to ensure consistent comparison.

### Corrected Version of the Function:

```python
def equals(self, other):
    self_axes, other_axes = self.axes, other.axes
    if len(self_axes) != len(other_axes) or not all(ax1.equals(ax2) for ax1, ax2 in zip(self_axes, other_axes)):
        return False

    self._consolidate_inplace()
    other._consolidate_inplace()
    
    if len(self.blocks) != len(other.blocks):
        return False

    def canonicalize(block):
        return (type(block).__name__, block.mgr_locs.as_array.tolist())

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)

    return all(block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks))
```

By incorporating the sorting based on block type name and locations, the corrected version will correctly compare the blocks of the `BlockManager` objects and return the expected result, resolving the issue reported in GitHub.