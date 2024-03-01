### Bug Explanation
The bug in the `equals` function arises due to the sorting method used for the `self_blocks` and `other_blocks` lists. The `canonicalize` function aims to sort the blocks based on their type names and `mgr_locs`, but it incorrectly uses `mgr_locs.as_array.tolist()` which returns a list instead of a tuple. This causes the sorting to fail and leads to incorrect comparison results.

### Bug Fix Strategy
To fix the bug, we need to modify the `canonicalize` function to correctly return a tuple combining the type name and `mgr_locs`. This change will ensure that the sorting method works as intended and the comparison between blocks is accurate.

### Corrected Version
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
        return (type(block).__name__, block.mgr_locs)

    self_blocks = sorted(self.blocks, key=canonicalize)
    other_blocks = sorted(other.blocks, key=canonicalize)
    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

By modifying the `canonicalize` function to return a tuple of type name and `mgr_locs`, the bug in the sorting logic is resolved. This corrected version should now provide the expected output values for the failing test cases.