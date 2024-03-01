### Bug Explanation
- The buggy function `equals` is not comparing the blocks properly due to the sorting method used for `self_blocks` and `other_blocks`.
- The sorting is done based on a tuple of block type and location, but it fails to differentiate when the order is changed for categorical blocks or others.
- This leads to wrongly returning `True` even when the blocks have different locations.

### Fix Strategy
- The fix involves ensuring that the location difference is considered correctly while comparing the blocks.
- Instead of just sorting by block type and location, we need to consider the block content for equality checks.

### Corrected Version
```python
# The corrected version of the buggy function
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
        self.blocks[i].equals(other.blocks[i]) for i in range(len(self.blocks))
    )
```

By iterating over the blocks directly and checking for equality individually, we ensure that the block content and locations are accurately compared. This change should solve the issue and return the correct result in cases like the failing test mentioned.