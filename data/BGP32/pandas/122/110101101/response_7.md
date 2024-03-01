### Bug Explanation
The bug in the `equals` function arises from the incorrect comparison of blocks between two `BlockManager` objects. The function tries to sort and compare the blocks based on their `dtype.name` and `mgr_locs`, but it fails due to the unconsolidated blocks that have a different order than expected. 

The bug causes the function to return `False` incorrectly when comparing two `BlockManager` objects where the blocks are not consolidated in the same order.

### Bug Fix Strategy
To fix the bug, we need to ensure that the blocks are consolidated and ordered correctly before comparing them. We can consolidate the blocks based on their order to prevent the issue with unconsolidated blocks affecting the comparison.

### Corrected Version of the `equals` Function

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

    # consolidate and sort blocks based on dtype.name
    self_blocks = sorted(self.blocks, key=lambda block: block.dtype.name)
    other_blocks = sorted(other.blocks, key=lambda block: block.dtype.name)

    return all(
        block.equals(oblock) for block, oblock in zip(self_blocks, other_blocks)
    )
``` 

With this corrected version, the `equals` function will first consolidate the blocks before sorting and comparing them. This approach should address the issue with the unconsolidated blocks and enable the correct comparison between two `BlockManager` objects.