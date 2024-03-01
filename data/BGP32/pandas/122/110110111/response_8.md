### Bug Explanation:
- The `equals` function in the `BlockManager` class tries to compare two instances of `BlockManager` based on their axes and blocks.
- The bug occurs because the function does not correctly compare the blocks between the two `BlockManager` instances.
- On line 25, the function sorts the blocks of both instances based on a combination of type name and location. This can lead to incorrect comparisons if blocks with the same data but different locations are present.
- The bug causes the function to incorrectly return `True` even when the blocks are not equal but have different locations.

### Bug Fix Strategy:
- To fix the bug, we need to compare the blocks directly without sorting them based on type and location.
- We can loop through the blocks of both instances simultaneously and check for equality of each pair.
- By doing this, we ensure that the comparison is done on the actual block data, not their locations.

### Corrected Code:
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

    return all(
        block.equals(oblock) for block, oblock in zip(self.blocks, other.blocks)
    )
```

By implementing the corrected code, the `equals` function should now correctly compare the `BlockManager` instances without considering block locations, ensuring the expected behavior.