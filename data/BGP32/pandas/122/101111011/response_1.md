### Explanation:
The buggy function `equals` in the `BlockManager` class fails to correctly compare two `BlockManager` instances containing blocks with different locations but identical values. The function sorts the blocks based on `dtype.name` and `mgr_locs.as_array` before comparison. However, in some cases, blocks may have the same data but different locations due to inconsistencies in their creation.

The failing test `test_dataframe_not_equal` creates two `DataFrame` instances with identical content but different column order, leading to the `equals` function returning `True` incorrectly.

### Solution:
To fix this bug, we need to update the `equals` function to compare blocks solely by their content without considering their locations. We can achieve this by comparing blocks in the original order rather than sorting them based on their dtype and location. This change ensures that the function correctly identifies equal blocks regardless of their locations.

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

Applying this change, the `equals` function will correctly compare the blocks inside the `BlockManager` instances, passing the failing test and resolving the issue reported on GitHub.