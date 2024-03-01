### Bug Explanation
The `equals` function in the `BlockManager` class is currently flawed because it compares the blocks based on their order, dtype name, and location, which can lead to incorrectly identifying blocks as equal when they are not. This issue arises when blocks have identical data but are arranged differently.

### Bug Fix Strategy
To address this bug, the comparison logic needs to be improved. Instead of sorting the blocks based on dtype name and location, the comparison should focus on the actual data within the blocks to determine equality.

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

    # Compare block values directly
    self_blocks = self.blocks
    other_blocks = other.blocks
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
```

### Expected Outcome
The corrected version of the function should now correctly identify when two `BlockManager` instances are not equal even if their blocks have the same data but are arranged differently.

By implementing this improved comparison logic, the `equals` function will resolve the issue described on GitHub and pass the failing test scenario provided.