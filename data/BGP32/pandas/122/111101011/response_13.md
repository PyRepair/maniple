### Analysis:
1. The `equals` function in the `BlockManager` class is expected to compare two `BlockManager` instances for equality.
2. The function compares the axes, consolidates the blocks, sorts them based on certain criteria, and then checks if the blocks themselves are equal.
3. The bug seems to stem from incorrect handling of block sorting and comparison, as indicated by failing tests and the GitHub issue.
4. The failing test `test_dataframe_not_equal` compares two DataFrames with columns swapped, expecting `equals` to return `False`.
5. The current implementation of `equals` fails to handle this swap correctly, leading to incorrect equality evaluation.

### Suggested Fix:
1. To fix the bug, adjust the block canonicalization method to consider the block content itself, not just the metadata.
2. Modify the sorting logic to ensure that blocks with different orderings but the same content are considered equal.
3. Update the comparison step to compare blocks by content rather than order.

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

    # compare blocks based on content, not order
    def canonicalize(block):
        return block.values
    
    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

With this corrected version, the `equals` function should now handle the comparison of identical blocks with different locations correctly, resolving the issue reported on GitHub.