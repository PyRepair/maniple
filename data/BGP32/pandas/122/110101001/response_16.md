### Bug Explanation:

The bug in the `equals` function arises from the way blocks are being compared between two instances. The function sorts the blocks based on their `dtype.name` and `mgr_locs.as_array.tolist()`, which can be different even if the blocks have the same data. This discrepancy leads to incorrect comparison results.

### Bug Fix Strategy:

To fix the bug, we should compare the blocks directly based on their data values rather than sorting and comparing by `dtype.name` and `mgr_locs.as_array.tolist()`.

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

    return all(
        block.equals(oblock) for block, oblock in zip(self.blocks, other.blocks)
    )
``` 

With this corrected version, the blocks will be compared directly without the need for sorting by `dtype.name` and `mgr_locs.as_array.tolist()`, which resolves the bug.