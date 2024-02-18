Based on the provided information, the bug in the `equals` function of the BlockManager class seems to stem from the comparison and sorting of the blocks within the tuples `self.blocks` and `other.blocks`. The issue posted on GitHub also supports the fact that the function is returning True when it should be False for identical blocks with different locations.

To fix this bug, one approach is to sort the blocks based on a consistent rule that takes into account the contents of the blocks rather than their location. This can be achieved by modifying the `canonicalize` function to consider the actual values of the blocks for sorting, ensuring that the comparison is accurate regardless of block location.

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

    # compare and sort the blocks based on their values
    self_blocks = sorted(self.blocks, key=lambda block: block.values)
    other_blocks = sorted(other.blocks, key=lambda block: block.values)
    
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

By modifying the sorting logic to consider the actual values of the blocks, we ensure that the comparison is based on the content rather than the block location. This should resolve the issue posted on GitHub and address the discrepancies in the comparison logic.